import os
from meals import *
import openai
from dotenv import load_dotenv
from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, url_for

# from openpyxl import load_workbook

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


if __name__ == "__main__":
    app.run(debug=True)