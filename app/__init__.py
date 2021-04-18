from . import log
from sqlite3 import ProgrammingError

from flask_migrate import Migrate
from sqlalchemy_utils import create_view

from .database.view import create_view_statement
from .database.models import db
from app.api.manage_api import manage_bp
from app.api.client_api import client_bp
import app.services.database_service as db_service

from flask import Flask
from app.config import Config
from app.tasks.background_task import run_scheduled_tasks
from flasgger import Swagger

migrate = Migrate()
logger = log.setup_custom_logger('app')


def init_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    config = Config()
    logger.info(config.SQLALCHEMY_DATABASE_URI)
    app.config.from_object(config)
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        app.register_blueprint(client_bp)
        app.register_blueprint(manage_bp)

        swagger = Swagger(app)
        # Create database views and tables
        create_views()
        create_tables()
        run_scheduled_tasks()
        return app


def create_tables():
    try:
        db.create_all()
    except:
        logger.error("Failed to recreat tables")


def create_views():
    try:
        statement = create_view_statement(db)
        create_view('table_view', statement, db.metadata)
    except ProgrammingError:
        logger.error("View already exists")

