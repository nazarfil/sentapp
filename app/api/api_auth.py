# Basic auth
from os import environ

from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

from app import Config

auth = HTTPBasicAuth()

config = Config()
users = {
    config.API_OAUTH_USERNAME: generate_password_hash(config.API_OAUTH_PASSWORD)
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username