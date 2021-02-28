from sqlite3 import ProgrammingError

from flask import Flask
from flask_migrate import Migrate

from sqlalchemy_utils import create_view
from .jobs.calculate_mean_socre import mean_score_from_csv, hype_score_from_csv
from .models import db, SentimentMeanScore, InputData, SentimentHypeScore
from app.jobs.populate_input_data import populate_db, update_populate_db
from app.jobs.twitter_scrape_job import scrape_twitter_from_csv
from app.jobs.populate_sentiment_for_input import calculate_sentiment
from .routes import bp
from celery import Celery
import app.services.database_service as db_service

migrate = Migrate()

def init_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    user = "user"
    password = "test"
    db_name = "db"
    host = "localhost"
    DATABSE_URI = 'postgresql://{user}:{password}@{server}/{database}'.format(user=user, password=password, server=host,
                                                                              database=db_name)
    print(DATABSE_URI)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABSE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        app.register_blueprint(bp)
        #
        celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
        celery.conf.update(app.config)
        #@populate_db()
        #scrape_twitter_from_csv()
        #calculate_sentiment()
        #mean_score_from_csv()
        #update_populate_db()
        # hype_score_from_csv()
        # sum_score_from_csv()
        try:
            statement = db_service.create_view_statement(db)
            create_view('table_view_max', statement, db.metadata)
        except ProgrammingError:
            print("View already exists")
        try :
            db.create_all()
        except:
            print("Tables already created")
        return app
