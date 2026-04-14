from app import db
from datetime import datetime

class Plan(db.Model):
    __tablename__ = "plans"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price_monthly = db.Column(db.Numeric(10, 2), nullable=False)
    price_yearly = db.Column(db.Numeric(10, 2), nullable=True)
    features = db.Column(db.JSON, default=dict)
    stripe_price_id_monthly = db.Column(db.String(255), nullable=True)
    stripe_price_id_yearly = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    subscriptions = db.relationship("Subscription", back_populates="plan")

class Subscription(db.Model):
    __tablename__ = "subscriptions"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    plan_id = db.Column(db.Integer, db.ForeignKey("plans.id"), nullable=False)
    status = db.Column(db.String(50), default="trialing")
    billing_cycle = db.Column(db.String(20), default="monthly")
    current_period_start = db.Column(db.DateTime, default=datetime.utcnow)
    current_period_end = db.Column(db.DateTime, nullable=False)
    stripe_subscription_id = db.Column(db.String(255), nullable=True)
    canceled_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    plan = db.relationship("Plan", back_populates="subscriptions")
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "plan_id": self.plan_id,
            "status": self.status,
            "billing_cycle": self.billing_cycle,
            "current_period_start": self.current_period_start.isoformat() if self.current_period_start else None,
            "current_period_end": self.current_period_end.isoformat() if self.current_period_end else None,
            "canceled_at": self.canceled_at.isoformat() if self.canceled_at else None,
        }
