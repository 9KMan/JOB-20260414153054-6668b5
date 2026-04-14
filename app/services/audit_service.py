from app import db
from app.models import AuditLog

def log_audit(user_id, action, entity_type=None, entity_id=None, ip_address=None, details=None):
    audit = AuditLog(
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        ip_address=ip_address,
        details=details
    )
    db.session.add(audit)
    db.session.commit()
    return audit
