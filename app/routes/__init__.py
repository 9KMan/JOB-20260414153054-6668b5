from flask import Blueprint

auth = Blueprint('auth', __name__, url_prefix='/api/auth')
users = Blueprint('users', __name__, url_prefix='/api/users')
dashboard = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')
subscriptions = Blueprint('subscriptions', __name__, url_prefix='/api/subscriptions')

from app.routes import auth_routes, users_routes, dashboard_routes, subscription_routes
