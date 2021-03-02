"""Flask configuration variables."""
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Set Flask configuration from .env file."""

    # General Config
    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')

    #TWITTER API TOKEN
    TWITTER_TOKEN = environ.get("TWITTER_TOKEN")
    if TWITTER_TOKEN is None:
        TWITTER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAEL3MgEAAAAA9YRG3JcE3J1UEr9ZgV4Acvpxe7A%3DuPoXPrxf1VFGtpeIxgWPq4i36YrTUfHrwqMEyG4Te5YBLj3Lf7'

    #Database
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    if SQLALCHEMY_DATABASE_URI is None:
        print("DB uri is not set, using default")
        SQLALCHEMY_DATABASE_URI='postgresql://user:test@localhost/db'
    SQLALCHEMY_DATABASE_PASSWORD = environ.get("SQLALCHEMY_DATABASE_PASSWORD")
    SQLALCHEMY_DATABASE_USERNAME = environ.get("SQLALCHEMY_DATABASE_USERNAME")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #CELERY QUEU ENDPOINT
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
