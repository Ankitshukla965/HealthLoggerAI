import os
from meals import *
import openai
from dotenv import load_dotenv

# from openpyxl import load_workbook

load_dotenv()



openai.api_key = os.getenv("OPENAI_API_KEY")
print(f"OPENAI_API_KEY from .env = {os.getenv('OPENAI_API_KEY')}")



food_input = input("What you want to track today: ")

meal = Meals(openai.api_key, food_input, "","","","", "")

meal.fetchMacros()

print(f"logging to excel")

log_to_excel(meal)

