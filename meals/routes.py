import os

from dotenv import load_dotenv
from flask import Blueprint, jsonify, redirect, render_template, request, url_for

from db import get_db
from meal_service import Meals, db_update

load_dotenv()

meal_bp = Blueprint("meal", __name__)


def meals_collection():
    return get_db()["meals"]


@meal_bp.route("/")
def home():
    return render_template("input.html")


@meal_bp.route("/submit", methods=["POST"])
def submit():
    food_input = (request.form.get("food_input") or "").strip()
    if not food_input:
        return jsonify({"error": "food_input is required"}), 400

    meal = Meals(os.getenv("OPENAI_API_KEY"), food_input)
    meal.fetchMacros()

    meals_collection().insert_one(db_update(meal))
    return redirect(url_for("meal.dashboard"))


@meal_bp.route("/dashboard", methods=["GET"])
def dashboard():
    all_meals = list(meals_collection().find())
    return render_template("index.html", meals=all_meals)


@meal_bp.route("/api/meals", methods=["GET", "POST"])
def meals_api():
    if request.method == "GET":
        all_meals = list(meals_collection().find({}, {"_id": 0}))
        return jsonify(all_meals), 200

    payload = request.get_json(silent=True) or {}
    food = (payload.get("food") or payload.get("name") or "").strip()
    if not food:
        return jsonify({"error": "Missing required field: food"}), 400

    if payload.get("compute", True):
        meal = Meals(os.getenv("OPENAI_API_KEY"), food)
        meal.fetchMacros()
        meal_doc = db_update(meal)
    else:
        meal_doc = {
            "food": food,
            "calories": payload.get("calories"),
            "protein": payload.get("protein"),
            "carbs": payload.get("carbs"),
            "fat": payload.get("fat"),
            "cholesterol": payload.get("cholesterol"),
        }

    meals_collection().insert_one(meal_doc)
    meal_doc.pop("_id", None)
    return jsonify({"status": "created", "meal": meal_doc}), 201
