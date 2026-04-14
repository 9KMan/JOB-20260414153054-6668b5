from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User
from app.routes import users
from app.services.audit_service import log_audit

@users.route('/', methods=['GET'])
@jwt_required()
def list_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '')
    
    query = User.query
    if search:
        query = query.filter(User.email.ilike(f'%{search}%') | User.full_name.ilike(f'%{search}%'))
    
    pagination = query.order_by(User.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'users': [u.to_dict() for u in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200

@users.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'user': user.to_dict()}), 200

@users.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user.is_admin and current_user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    if data.get('full_name'):
        user.full_name = data['full_name']
    if data.get('is_active') is not None and current_user.is_admin:
        user.is_active = data['is_active']
    if data.get('is_admin') is not None and current_user.is_admin:
        user.is_admin = data['is_admin']
    
    db.session.commit()
    log_audit(current_user_id, 'user_updated', 'user', user_id)
    
    return jsonify({'user': user.to_dict()}), 200

@users.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    db.session.delete(user)
    db.session.commit()
    log_audit(current_user_id, 'user_deleted', 'user', user_id)
    
    return jsonify({'message': 'User deleted'}), 200
