from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from config import config

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    from app.routes import auth, users, dashboard, subscriptions
    app.register_blueprint(auth.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(subscriptions.bp)
    
    @app.route('/health')
    def health():
        return {'status': 'healthy'}
    
    return app
