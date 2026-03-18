from datetime import timedelta

from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash


def hash_password(password):
    return generate_password_hash(password)


def verify_password(password, hashed_password):
    return check_password_hash(hashed_password, password)


def generate_token(identity):
    return create_access_token(identity=identity, expires_delta=timedelta(days=1))
