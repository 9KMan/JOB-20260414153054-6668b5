from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models.user import User
from models.audit_log import AuditLog

users_bp = Blueprint("users", __name__)

def get_current_user():
    return User.query.get(int(get_jwt_identity()))

@users_bp.route("/", methods=["GET"])
@jwt_required()
def list_users():
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 20, type=int), 100)
    search = request.args.get("search", "")
    
    query = User.query
    if search:
        query = query.filter(User.email.ilike(f"%{search}%") | User.full_name.ilike(f"%{search}%"))
    
    pagination = query.order_by(User.created_at.desc()).paginate(page=page, per_page=per_page)
    
    return jsonify({
        "users": [u.to_dict() for u in pagination.items],
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": page,
    }), 200

@users_bp.route("/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id):
    current_user = get_current_user()
    if current_user.role != "admin" and current_user.id != user_id:
        return jsonify({"error": "Unauthorized"}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({"user": user.to_dict(include_sensitive=True)}), 200

@users_bp.route("/<int:user_id>", methods=["PUT"])
@jwt_required()
def update_user(user_id):
    current_user = get_current_user()
    if current_user.role != "admin" and current_user.id != user_id:
        return jsonify({"error": "Unauthorized"}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    if "full_name" in data:
        user.full_name = data["full_name"].strip()
    if "email" in data:
        new_email = data["email"].strip().lower()
        if new_email != user.email and User.query.filter_by(email=new_email).first():
            return jsonify({"error": "Email already in use"}), 409
        user.email = new_email
    if "password" in data and data["password"]:
        if len(data["password"]) < 8:
            return jsonify({"error": "Password must be at least 8 characters"}), 400
        user.set_password(data["password"])
    if current_user.role == "admin":
        if "is_active" in data:
            user.is_active = bool(data["is_active"])
        if "role" in data:
            user.role = data["role"]
    
    db.session.commit()
    AuditLog(user_id=current_user.id, action="user.updated", resource="user", resource_id=user.id,
             details={"fields": list(data.keys())}).add(db.session)
    db.session.commit()
    
    return jsonify({"user": user.to_dict(), "message": "User updated successfully"}), 200

@users_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    current_user = get_current_user()
    if current_user.role != "admin":
        return jsonify({"error": "Admin access required"}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    if user.id == current_user.id:
        return jsonify({"error": "Cannot delete yourself"}), 400
    
    AuditLog(user_id=current_user.id, action="user.deleted", resource="user", resource_id=user.id).add(db.session)
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({"message": "User deleted successfully"}), 200
