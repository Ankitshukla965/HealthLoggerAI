from meals import *

# from openpyxl import load_workbook

api_key = "v"

food_input = input("What you want to track today: ")

meal = Meals(api_key, food_input, "","","","", "")

meal.fetchMacros()

print(f"logging to excel")

log_to_excel(meal)

