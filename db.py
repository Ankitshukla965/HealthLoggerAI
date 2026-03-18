from urllib.parse import urlparse

from flask import current_app
from pymongo import MongoClient


def init_mongo(app):
    uri = app.config["MONGO_URI"]
    client = MongoClient(uri)

    parsed = urlparse(uri)
    db_name = parsed.path.lstrip("/") or "healthlogger"

    app.extensions["mongo_client"] = client
    app.extensions["mongo_db"] = client[db_name]


def get_db():
    return current_app.extensions["mongo_db"]
