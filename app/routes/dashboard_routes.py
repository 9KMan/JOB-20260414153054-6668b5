from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
from app import db
from app.models import User, Subscription, Plan, AuditLog
from app.routes import dashboard

@dashboard.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    total_users = User.query.count()
    active_users = User.query.filter_by(is_active=True).count()
    active_subscriptions = Subscription.query.filter_by(status='active').count()
    total_plans = Plan.query.filter_by(is_active=True).count()
    
    recent_signups = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    return jsonify({
        'stats': {
            'total_users': total_users,
            'active_users': active_users,
            'active_subscriptions': active_subscriptions,
            'total_plans': total_plans,
        },
        'recent_signups': [u.to_dict() for u in recent_signups]
    }), 200

@dashboard.route('/activity', methods=['GET'])
@jwt_required()
def get_activity():
    page = 1
    per_page = 50
    
    pagination = AuditLog.query.order_by(AuditLog.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'activity': [a.to_dict() for a in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages
    }), 200
