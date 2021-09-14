import requests
import pandas as pd

NO_RECIPE = 'The recipe search requires input, please answer the questions! '
NO_CREDENTIALS = 'Please check the API Edamam recipe credentials are entered correctly: '

# function to connect with the API with error check
def recipe_search(ingredient, app_id, app_key, user_cook_time, mealType, max_results=5):
    # Register to get an APP ID and key https://developer.edamam.com/
    #app_id = 'f79ed4b2'
    #app_key = '758ec61e53ffcfdba764003d0c8ceb29'
    if ingredient is None:
        raise ValueError(NO_RECIPE)
    if app_id is None or app_id == '' or app_key is None or app_key == '':
        raise ValueError(NO_CREDENTIALS)

    result = requests.get(
    'https://api.edamam.com/search?q={}&app_id={}&app_key={}&user_cook_time={}&mealType={}'
    .format(ingredient, app_id, app_key, user_cook_time, mealType,  max_results))
    data = result.json()
    return data['hits']

# get input from User - API ID, API KEY, an ingredient, time allowance and meal type to start filtering the recipes
def get_recipes():
    app_id = input('Enter your API ID: ')
    app_key = input('Enter your API key: ')
    ingredient = input('Enter an ingredient(s): ')
    mealType = input('Please choose a meal type from Breakfast, Lunch, Dinner, Snack, Teatime: ')

#function to error check if user does not enter the time as a number
    def correct_time(time):
        global cook_time
        # check for number entered
        if time.isdigit():
            cook_time = f"&time={time}"
        else:
            print('Im sorry, please enter your time as a number (in minutes): ')
            #ask for input cook time again
            time_check = input('How much time do you have to cook (in minutes): ')
            correct_time(time_check)

        return cook_time

    time = input('How much time do you have to cook (in minutes): ')
    user_cook_time = correct_time(time)
    results = recipe_search(ingredient, app_id, app_key, user_cook_time, mealType)

#write results into a csv file displaying certain criteria
    with open('recipe.csv', 'w') as file:
        file.write('recipe_name,yield,calories,calories_per_serving,recipe_url,ingredients,recipe_image\n')
        for result in results:
            recipe_name = result['recipe']['label']
            recipe_yield = result['recipe']['yield']
            calories = result['recipe']['calories']
            calories_per_serving = int(result['recipe']['calories'] / int(result['recipe']['yield']))
            recipe_url = result['recipe']['url']
            ingredients = result['recipe']['ingredientLines']
            recipe_image = result['recipe']['image']

            file.write('{},{},{},{},{},{},{}\n'.format(recipe_name, recipe_yield, calories, calories_per_serving, recipe_url, ingredients, recipe_image))

#store the image as a png under the recipe name
            receive = requests.get(recipe_image)
            with open(r'{}.png'.format(recipe_name), 'wb') as f:
                f.write(receive.content)

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