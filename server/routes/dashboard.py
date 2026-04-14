from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models.user import User
from models.subscription import Subscription
from models.audit_log import AuditLog
from sqlalchemy import func, desc

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/stats", methods=["GET"])
@jwt_required()
def get_stats():
    current_user_id = int(get_jwt_identity())
    current_user = User.query.get(current_user_id)
    
    total_users = User.query.count()
    active_users = User.query.filter_by(is_active=True).count()
    total_subscriptions = Subscription.query.count()
    active_subscriptions = Subscription.query.filter_by(status="active").count()
    
    recent_signups = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(10).all()
    
    return jsonify({
        "stats": {
            "total_users": total_users,
            "active_users": active_users,
            "total_subscriptions": total_subscriptions,
            "active_subscriptions": active_subscriptions,
        },
        "recent_signups": [u.to_dict() for u in recent_signups],
        "recent_activity": [
            {
                "action": log.action,
                "resource": log.resource,
                "created_at": log.created_at.isoformat() if log.created_at else None,
            }
            for log in recent_logs
        ],
        "is_admin": current_user.role == "admin",
    }), 200

@dashboard_bp.route("/activity", methods=["GET"])
@jwt_required()
def get_activity():
    page = 1
    per_page = 50
    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).paginate(page=page, per_page=per_page)
    
    return jsonify({
        "activity": [
            {
                "id": log.id,
                "user_id": log.user_id,
                "action": log.action,
                "resource": log.resource,
                "resource_id": log.resource_id,
                "ip_address": log.ip_address,
                "created_at": log.created_at.isoformat() if log.created_at else None,
            }
            for log in logs.items
        ],
        "total": logs.total,
        "pages": logs.pages,
    }), 200
