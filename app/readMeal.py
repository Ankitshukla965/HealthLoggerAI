import meals
from openpyxl import load_workbook



def read_from_excel():
            wb = load_workbook('CalorieTracker.xlsx')

            ws = wb['Macros']
            tracked_meals = []

            headers = [cell.value for cell in ws[1]]

            # print(headers)
            #Appending the Meals to the Meals dictionary
            for row in ws.iter_rows(min_row=2, values_only=True):
                meal = {headers[i]: row[i] for i in range(len(headers))}
                tracked_meals.append(meal)
            # print(meals)
            return tracked_meals


#Data structures method

tracked_meals = read_from_excel()
tracked_meals = [meal for meal in tracked_meals if meal['Food']  is not None]
print(tracked_meals)
# unique_foods = set(meal['Protein'] for meal in tracked_meals if meal['Protein'] is not None)
# print(unique_foods)

sorted_meals = sorted(tracked_meals, key=lambda meal: int(meal['Protein']), reverse=True)


protein_values = [meal['Protein'] for meal in tracked_meals if meal['Protein'] is not None]
print(protein_values)