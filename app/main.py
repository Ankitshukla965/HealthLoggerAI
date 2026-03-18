import os
from meals import *
import openai
from dotenv import load_dotenv
from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, url_for, jsonify
from auth.routes import auth_bp 
from pathlib import Path
# from openpyxl import load_workbook
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv()

#Connecting to Mongo DB

client =  MongoClient(os.getenv("MONGO_URI"))
databases = client.list_database_names()
print("✅ MongoDB Connection Successful!")
db = client["HealthLogger"]
meals_collection = db["meals"]

openai.api_key = os.getenv("OPENAI_API_KEY")
# print(f"OPENAI_API_KEY from .env = {os.getenv('OPENAI_API_KEY')}")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "..", "templates")

app = Flask(__name__, template_folder=TEMPLATE_DIR )


@app.route('/')
def home():
      print("Home Page Loaded")
      return render_template("input.html")

@app.route('/submit', methods=["POST"])
def submit():
      print("Submit called")
      food_input = request.form.get("food_input")
      meal = Meals(openai.api_key, food_input, "","","","", "")
      meal.fetchMacros()
      
      
      meal_doc = db_update(meal)
      meals_collection.insert_one(meal_doc)
      return redirect(url_for("dashboard"))

@app.route('/dashboard', methods=["GET"])
def dashboard():
    
    all_meals = list(meals_collection.find())
    # print("all_meals = ",all_meals)
    # for meal in all_meals:
    #      print(meal['food'])
    
    return render_template("index.html", meals = all_meals)

@app.route("/api/meals", methods=["GET", "POST"])
def meals_api():
    if request.method == "GET":
        all_meals = list(meals_collection.find({}, {"_id": 0}))
        return jsonify(all_meals), 200

    # POST
    payload = request.get_json(silent=True) or {}

    food = (payload.get("food") or payload.get("name") or "").strip()
    if not food:
        return jsonify({"error": "Missing required field: food"}), 400

    # Option A: compute macros using your existing OpenAI flow
    if payload.get("compute", True):
        meal = Meals(openai.api_key, food, "", "", "", "", "")
        meal.fetchMacros()
        meal_doc = db_update(meal)   # your existing mapper
    else:
        # Option B: accept macros directly
        meal_doc = {
            "food": food,
            "calories": payload.get("calories"),
            "protein": payload.get("protein"),
            "carbs": payload.get("carbs"),
            "fat": payload.get("fat"),
        }

    # store
    meals_collection.insert_one(meal_doc)

    # return without Mongo _id
    meal_doc.pop("_id", None)
    return jsonify({"status": "created", "meal": meal_doc}), 201


app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == "__main__":
    app.run(debug=True)  
