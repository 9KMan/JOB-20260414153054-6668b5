from models.audit_log import AuditLog

class AuditService:
    @staticmethod
    def log(user_id, action, resource=None, resource_id=None, details=None, ip_address=None, user_agent=None, db_session=None):
        log = AuditLog(
            user_id=user_id,
            action=action,
            resource=resource,
            resource_id=resource_id,
            details=details or {},
            ip_address=ip_address,
            user_agent=user_agent,
        )
        if db_session:
            db_session.add(log)
        return log

    @staticmethod
    def get_user_activity(user_id, limit=50):
        return AuditLog.query.filter_by(user_id=user_id).order_by(AuditLog.created_at.desc()).limit(limit).all()

    @staticmethod
    def get_resource_history(resource, resource_id, limit=50):
        return AuditLog.query.filter_by(resource=resource, resource_id=resource_id).order_by(AuditLog.created_at.desc()).limit(limit).all()
