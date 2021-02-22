
from flask import Flask
from flask_migrate import Migrate
from .models import db
from app.jobs.populate_input_data import populate_db
from app.jobs.twitter_scrape_job import scrape_twitter_from_csv
from app.jobs.populate_sentiment_for_input import calculate_sentiment
from .routes import bp
from celery import Celery

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
        #populate_db()
        #scrape_twitter_from_csv()
        #calculate_sentiment()
        return app


