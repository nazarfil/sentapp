# Basic auth
from os import environ

from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

auth = HTTPBasicAuth()
USERNAME = environ.get('MANAGE_USER')
PASSWORD = environ.get('MANAGE_PASSWORD')
if USERNAME is None or PASSWORD is None:
    USERNAME = "user"
    PASSWORD = "test"

users = {
    USERNAME: generate_password_hash(PASSWORD)
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username