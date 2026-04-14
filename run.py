from app import create_app, db
from app.models import User, Plan, Subscription, AuditLog

app = create_app('development')

@app.shell_context_processor
def shell():
    return {'db': db, 'User': User, 'Plan': Plan, 'Subscription': Subscription, 'AuditLog': AuditLog}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
