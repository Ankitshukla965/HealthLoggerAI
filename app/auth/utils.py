from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta

bcrypt = Bcrypt()

def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.check_password_hash(hashed, password)

def generate_token(identity):
    return create_access_token(identity=identity, expires_delta=timedelta(days=1))