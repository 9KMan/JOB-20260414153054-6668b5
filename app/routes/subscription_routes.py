from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Subscription, Plan, User
from app.routes import subscriptions
from app.services.audit_service import log_audit
from datetime import datetime, timedelta

@subscriptions.route('/', methods=['GET'])
@jwt_required()
def list_subscriptions():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status', '')
    
    query = Subscription.query
    if status:
        query = query.filter_by(status=status)
    
    pagination = query.order_by(Subscription.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'subscriptions': [s.to_dict() for s in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200

@subscriptions.route('/<int:subscription_id>', methods=['GET'])
@jwt_required()
def get_subscription(subscription_id):
    subscription = Subscription.query.get(subscription_id)
    if not subscription:
        return jsonify({'error': 'Subscription not found'}), 404
    return jsonify({'subscription': subscription.to_dict()}), 200

@subscriptions.route('/', methods=['POST'])
@jwt_required()
def create_subscription():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    plan_id = data.get('plan_id')
    if not plan_id:
        return jsonify({'error': 'Plan ID required'}), 400
    
    plan = Plan.query.get(plan_id)
    if not plan or not plan.is_active:
        return jsonify({'error': 'Invalid or inactive plan'}), 400
    
    expires_at = datetime.utcnow() + timedelta(days=30)
    
    subscription = Subscription(
        user_id=user_id,
        plan_id=plan_id,
        status='active',
        expires_at=expires_at
    )
    db.session.add(subscription)
    db.session.commit()
    
    log_audit(user_id, 'subscription_created', 'subscription', subscription.id)
    
    return jsonify({'subscription': subscription.to_dict()}), 201

@subscriptions.route('/<int:subscription_id>', methods=['PUT'])
@jwt_required()
def update_subscription(subscription_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    subscription = Subscription.query.get(subscription_id)
    if not subscription:
        return jsonify({'error': 'Subscription not found'}), 404
    
    data = request.get_json()
    if data.get('status'):
        subscription.status = data['status']
    if data.get('expires_at'):
        subscription.expires_at = datetime.fromisoformat(data['expires_at'])
    
    db.session.commit()
    log_audit(current_user_id, 'subscription_updated', 'subscription', subscription_id)
    
    return jsonify({'subscription': subscription.to_dict()}), 200

@subscriptions.route('/plans', methods=['GET'])
@jwt_required()
def list_plans():
    plans = Plan.query.filter_by(is_active=True).all()
    return jsonify({'plans': [p.to_dict() for p in plans]}), 200
