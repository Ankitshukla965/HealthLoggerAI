import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'supersecretkey')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwtsecret')
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/healthlogger')