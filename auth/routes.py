from flask import Blueprint, jsonify, request

from auth.utils import generate_token, hash_password, verify_password
from db import get_db

auth_bp = Blueprint("auth", __name__)


def users_collection():
    return get_db()["users"]


@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    if users_collection().find_one({"email": email}):
        return jsonify({"error": "User already exists"}), 409

    users_collection().insert_one(
        {
            "email": email,
            "password": hash_password(password),
        }
    )
    return jsonify({"message": "Signup successful"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip()
    password = data.get("password") or ""

    user = users_collection().find_one({"email": email})
    if not user or not verify_password(password, user["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token(identity=email)
    return jsonify({"token": token}), 200
