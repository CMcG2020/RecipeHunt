import requests
import pandas as pd

# function to connect with the API
def recipe_search(ingredient, time, mealType):
    # Register to get an APP ID and key https://developer.edamam.com/
    app_id = 'f79ed4b2'
    app_key = '758ec61e53ffcfdba764003d0c8ceb29'
    result = requests.get(
    'https://api.edamam.com/search?q={}&app_id={}&app_key={}&time={}'
    .format(ingredient, app_id,app_key, time, mealType))
    data = result.json()
    return data['hits']

# get input from User - an ingredient and time allowance to filter the recipes
def get_recipes():
    ingredient = input('Enter an ingredient: ')
    time = input('How much time do you have to cook: ')
    mealType = input('Please chose a meal type: Breakfast, Dinner, Lunch, Snack, Teatime: ')
    results = recipe_search(ingredient, time, mealType)

    with open('recipe.csv', 'w') as file:
        file.write('recipe_name,calories,calories_per_serving,recipe_url,ingredients\n')
        for result in results:
            recipe_name = result['recipe']['label']
            calories = result['recipe']['calories']
            calories_per_serving = int(result['recipe']['calories'] / int(result['recipe']['yield']))
            recipe_url = result['recipe']['url']
            ingredients = result['recipe']['ingredients']
            file.write('{},{},{},{}\n'.format(recipe_name, calories, calories_per_serving, recipe_url,ingredients))

# sort the file and display the top 5 results by calories
def sort_file():
    df = pd.read_csv('recipe.csv', encoding='unicode_escape')
    df = df.sort_values(by=['calories_per_serving'], ascending=True)
    df.to_csv('recipe.csv', index=False)
 
 
def display_top_5():
    df = pd.read_csv('recipe.csv', encoding='unicode_escape')
    print(df.head(5))

# main function
def main():
    get_recipes()
    sort_file()
    display_top_5()

main()