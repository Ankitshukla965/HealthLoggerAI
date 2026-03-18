from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from db import init_mongo
from auth.routes import auth_bp
from users.routes import user_bp
from meals.routes import meal_bp

try:
    from flask_cors import CORS
except ModuleNotFoundError:
    def CORS(_app):
        return _app

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
JWTManager(app)
init_mongo(app)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(meal_bp)

if __name__ == "__main__":
    app.run(debug=True)
