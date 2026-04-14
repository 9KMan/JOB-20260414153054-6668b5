from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models.user import User
from models.subscription import Subscription, Plan
from models.audit_log import AuditLog
from datetime import datetime, timedelta

subscriptions_bp = Blueprint("subscriptions", __name__)

def get_current_user():
    return User.query.get(int(get_jwt_identity()))

@subscriptions_bp.route("/plans", methods=["GET"])
def list_plans():
    plans = Plan.query.filter_by(is_active=True).all()
    return jsonify({
        "plans": [
            {
                "id": p.id,
                "name": p.name,
                "price_monthly": float(p.price_monthly),
                "price_yearly": float(p.price_yearly) if p.price_yearly else None,
                "features": p.features or {},
            }
            for p in plans
        ]
    }), 200

@subscriptions_bp.route("/", methods=["GET"])
@jwt_required()
def get_subscription():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user or not user.subscription_id:
        return jsonify({"subscription": None, "plan": None}), 200
    
    sub = Subscription.query.get(user.subscription_id)
    if not sub:
        return jsonify({"subscription": None, "plan": None}), 200
    
    plan = Plan.query.get(sub.plan_id)
    return jsonify({
        "subscription": sub.to_dict(),
        "plan": {
            "id": plan.id,
            "name": plan.name,
            "price_monthly": float(plan.price_monthly),
            "features": plan.features or {},
        } if plan else None,
    }), 200

@subscriptions_bp.route("/", methods=["POST"])
@jwt_required()
def create_subscription():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    if not data or not data.get("plan_id"):
        return jsonify({"error": "plan_id is required"}), 400
    
    plan = Plan.query.get(data["plan_id"])
    if not plan or not plan.is_active:
        return jsonify({"error": "Invalid or inactive plan"}), 400
    
    user = User.query.get(user_id)
    if user.subscription_id:
        return jsonify({"error": "Subscription already exists"}), 409
    
    billing_cycle = data.get("billing_cycle", "monthly")
    if billing_cycle not in ("monthly", "yearly"):
        return jsonify({"error": "billing_cycle must be 'monthly' or 'yearly'"}), 400
    
    now = datetime.utcnow()
    period_end = now + timedelta(days=30 if billing_cycle == "monthly" else 365)
    
    sub = Subscription(
        user_id=user_id,
        plan_id=plan.id,
        status="trialing",
        billing_cycle=billing_cycle,
        current_period_start=now,
        current_period_end=period_end,
    )
    db.session.add(sub)
    db.session.flush()
    
    user.subscription_id = sub.id
    db.session.commit()
    
    AuditLog(user_id=user_id, action="subscription.created", resource="subscription", resource_id=sub.id,
             details={"plan_id": plan.id, "billing_cycle": billing_cycle}).add(db.session)
    db.session.commit()
    
    return jsonify({"subscription": sub.to_dict(), "message": "Subscription created"}), 201

@subscriptions_bp.route("/<int:sub_id>/cancel", methods=["POST"])
@jwt_required()
def cancel_subscription(sub_id):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    sub = Subscription.query.get(sub_id)
    if not sub or sub.user_id != user_id:
        return jsonify({"error": "Subscription not found"}), 404
    
    sub.status = "canceled"
    sub.canceled_at = datetime.utcnow()
    db.session.commit()
    
    AuditLog(user_id=user_id, action="subscription.canceled", resource="subscription", resource_id=sub.id).add(db.session)
    db.session.commit()
    
    return jsonify({"subscription": sub.to_dict(), "message": "Subscription canceled"}), 200
