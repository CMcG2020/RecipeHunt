import requests
import csv
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

   
# make a file to store the results
def make_csv(results):
    with open('recipe.csv', 'w') as csvfile:
        fieldnames = ['recipe_name', 'recipe_url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result)

# sort the results
def sort_csv():
    df = pd.read_csv('recipe.csv')
    df = df.sort_values(by=['recipe_name'])
    df.to_csv('recipe.csv', index=False)

# display the results
def display_results():
    df = pd.read_csv('recipe.csv')
    print(df.head())

# main function
def main():
    results = get_recipes()
    make_csv(results)
    sort_csv()
    display_results()

main()