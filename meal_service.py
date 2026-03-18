import datetime
import re

from openai import OpenAI
from openpyxl import load_workbook


class Meals:
    def __init__(self, api_key, food_name, calories=None, protein=None, carbohydrates=None, fats=None, cholesterol=None):
        self.food_name = food_name
        self.calories = calories
        self.protein = protein
        self.carbohydrates = carbohydrates
        self.fats = fats
        self.cholesterol = cholesterol
        self.api_key = api_key

    def fetchMacros(self):
        client = OpenAI(api_key=self.api_key)
        prompt = f"""
Estimate the calories, protein, carbohydrates, fats, and cholesterol for {self.food_name}.
Return only this format:
Calories: <number>
Protein: <number>
Carbohydrates: <number>
Fats: <number>
Cholesterol: <number>
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful nutritionist.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            max_tokens=100,
            temperature=0.8,
        )

        reply = (response.choices[0].message.content or "").strip()

        self.calories = self._extract_macros(reply, r"Calories:\s*(\d+)")
        self.protein = self._extract_macros(reply, r"Protein:\s*(\d+)")
        self.carbohydrates = self._extract_macros(reply, r"Carbohydrates:\s*(\d+)")
        self.fats = self._extract_macros(reply, r"Fats:\s*(\d+)")
        self.cholesterol = self._extract_macros(reply, r"Cholesterol:\s*(\d+)")

    def _extract_macros(self, reply, pattern):
        match = re.search(pattern, reply, re.IGNORECASE)
        return match.group(1) if match else None

    def __str__(self):
        return (
            f"Food: {self.food_name}\n"
            f"Calories: {self.calories}\n"
            f"Protein: {self.protein}\n"
            f"Carbohydrates: {self.carbohydrates}\n"
            f"Fats: {self.fats}\n"
            f"Cholesterol: {self.cholesterol}\n"
        )


def log_to_excel(meal):
    date_today = datetime.datetime.today().strftime("%d/%m/%Y")
    wb = load_workbook("CalorieTracker.xlsx")
    ws = wb["Macros"]
    ws.append(
        [
            date_today,
            meal.food_name,
            meal.calories,
            meal.protein,
            meal.carbohydrates,
            meal.fats,
            meal.cholesterol,
        ]
    )
    wb.save("CalorieTracker.xlsx")


def db_update(meal):
    date_today = datetime.datetime.today().strftime("%d/%m/%Y")
    return {
        "date": date_today,
        "food": meal.food_name,
        "calorie": meal.calories,
        "protein": meal.protein,
        "carbs": meal.carbohydrates,
        "fat": meal.fats,
        "cholesterol": meal.cholesterol,
    }
