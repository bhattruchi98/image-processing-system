from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from celery import Celery
from .config import Config

db = SQLAlchemy()

# Initialize Celery
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)  # Add this line to initialize Flask-Migrate

    # Register blueprints
    from .api import api_bp
    app.register_blueprint(api_bp)

    return app