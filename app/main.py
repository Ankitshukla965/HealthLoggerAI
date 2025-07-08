from meals import *

# from openpyxl import load_workbook

api_key = "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"

food_input = input("What you want to track today: ")

meal = Meals(api_key, food_input, "","","","", "")

meal.fetchMacros()

print(f"logging to excel")

log_to_excel(meal)

