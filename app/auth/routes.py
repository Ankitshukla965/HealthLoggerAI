from flask import Blueprint, request, jsonify
from auth.utils import hash_password, check_password, generate_token
from db import db

auth_bp = Blueprint('auth', __name__)
users_collection = db["users"]

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    if users_collection.find_one({"email": email}):
        return jsonify({"error": "User already exists"}), 409

    hashed_pw = hash_password(password)
    users_collection.insert_one({"email": email, "password": hashed_pw})
    print(hashed_pw)
    return jsonify({"message": "Signup successful"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = users_collection.find_one({"email": email})
    if not user or not check_password(password, user["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token(identity=email)
    return jsonify({"token": token}), 200