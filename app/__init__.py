from flask import Flask
from flask_migrate import Migrate
from .models import db
from app.jobs.populate_input_data import populate_db
from app.jobs.twitter_scrape_job import scrape_twitter_from_csv
from .routes import bp


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
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        app.register_blueprint(bp)
        #populate_db()
        scrape_twitter_from_csv()
        return app
