from flask_migrate import Migrate
from .jobs.calculate_hype_score_job import mean_score_from_csv, hype_score_from_csv
from .models import db, SentimentMeanScore, InputData, SentimentHypeScore
from app.jobs.populate_input_data_job import populate_db_from_csv, update_populate_db
from app.jobs.twitter_scrape_job import scrape_twitter_from_csv
from app.jobs.populate_sentiment_for_input_job import calculate_sentiment
from app.api.manage_api import manage_bp
from app.api.client_api import client_bp
import app.services.database_service as db_service
from flask import Flask
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
        app.register_blueprint(client_bp)
        app.register_blueprint(manage_bp)
        try :
            db.create_all()
        except :
            print("Failed to recreat tables")
        return app
