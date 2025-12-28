from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from db import mongo
from auth.routes import auth_bp
from users.routes import user_bp
from meals.routes import meal_bp

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
JWTManager(app)
mongo.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(meal_bp, url_prefix='/meal')

if __name__ == '__main__':
    app.run(debug=True)