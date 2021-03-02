from sqlite3 import ProgrammingError

from flask import Flask
from flask_migrate import Migrate

from sqlalchemy_utils import create_view
from .jobs.calculate_mean_socre import mean_score_from_csv, hype_score_from_csv
from .models import db, SentimentMeanScore, InputData, SentimentHypeScore
from app.jobs.populate_input_data import populate_db_from_csv, update_populate_db
from app.jobs.twitter_scrape_job import scrape_twitter_from_csv
from app.jobs.populate_sentiment_for_input import calculate_sentiment
from .routes import bp
from celery import Celery
import app.services.database_service as db_service
from app.config import Config

migrate = Migrate()


def init_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    config = Config()
    print(config.SQLALCHEMY_DATABASE_URI)
    app.config.from_object(config)
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        app.register_blueprint(bp)
        #
        #celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
        #celery.conf.update(app.config)
        try:
            statement = db_service.create_view_statement(db)
            create_view('table_view_max', statement, db.metadata)
        except ProgrammingError:
            print("View already exists")
        try:
            db.create_all()
        except:
            print("Tables already created")

        return app


