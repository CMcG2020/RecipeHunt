
import requests


NO_RECIPE = 'The recipe search requires input, please answer the questions! '
NO_CREDENTIALS = 'Please check the API EDAMAM recipe credentials are entered correctly: '


# function to connect with the API with error check
def recipe_search(ingredient, app_id, app_key, user_cook_time, user_meal_type, max_results=5):
    # Register to get an APP ID and key https://developer.edamam.com/
    # app_id = f79ed4b2
    # app_key = 758ec61e53ffcfdba764003d0c8ceb29
    if ingredient is None:
        raise ValueError(NO_RECIPE)
    if app_id is None or app_id == '' or app_key is None or app_key == '':
        raise ValueError(NO_CREDENTIALS)

    result = requests.get(
        f'https://api.edamam.com/search?q={ingredient}&app_id={app_id}&app_key={app_key}&time={user_cook_time}&mealType={user_meal_type}&from=0&to={max_results}')
    data = result.json()
    return data['hits']


# get input from User - API ID, API KEY, an ingredient, time allowance and meal type to start filtering the recipes
def get_recipes():
    global recipe_image, recipe_name
    app_id = input('Enter your API ID: ')
    app_key = input('Enter your API key: ')

    # ask for ingredient, check that it is a valid word entered.
    ingredient = input('Enter an ingredient(s): ')
    def ingredient_check (ingredient):
        if ingredient.isdigit():
            bad_ingredient = input('Im sorry, please enter a valid ingredient: ')
            ingredient_check(bad_ingredient)
        else:
            return ingredient

    # function to error check user input for meal_type
    meals = ['breakfast', 'lunch', 'dinner', 'snack', 'teatime']
    def check_meal_type(meal_type):
        if meal_type not in meals:
            meal_type_check = input(
                'Please choose a meal type from Breakfast, Lunch, Dinner, Snack, Teatime: ').lower()
            check_meal_type(meal_type_check)
        else:
            return meal_type

    meal_type = input('Please choose a meal type from Breakfast, Lunch, Dinner, Snack, Teatime: ').lower()
    user_meal_type = check_meal_type(meal_type)

    # function to error check if user does not enter the time as a number
    def correct_time(time):
        # check for number entered
        if time.isdigit():
            cook_time = str(time)
        else:
            print('Im sorry, please enter your time as a number (in minutes)! ')
            # ask for input cook time again
            time_check = input('How much time do you have to cook (in minutes): ')
            correct_time(time_check)

        return cook_time

    time = input('How much time do you have to cook (in minutes): ')
    user_cook_time = correct_time(time)
    results = recipe_search(ingredient, app_id, app_key, user_cook_time, meal_type)

    # write results into a csv file displaying certain criteria
    with open('recipes.txt', 'w') as file:
        for recipe in results:
            recipe_data = recipe['recipe']
            # find serving size for each recipe and calculate calories per serving
            calories_per_serving = int(recipe_data['calories'] / int(recipe_data['yield']))
            file.write('Recipe: ' + recipe_data['label'] + '\n')
            file.write('Total Calories: ' + str(recipe_data['calories']) + '\n')
            file.write('Calories per serving: ' + str(calories_per_serving) + '\n')
            file.write('Time to cook: ' + str(recipe_data['totalTime']) + '\n')
            file.write('Ingredients: ' + str(recipe_data['ingredientLines']) + '\n')
            file.write('Link: ' + recipe_data['url'] + '\n')
            file.write('Image: ' + recipe_data['image'] + '\n')
            file.write('\n')
    file.close()
    return results





'''# sort the file using the calorie classification
def my_sort(results):
    calorie_class = {'LOW': ,
                    'MEDIUM': 600,
                    'HIGH': 1000,
                    }
    results_fields = line.strip().split()
    meal_class = results_fields[-1]
    return calorie_class[meal_class]

# reading recipes.txt and storing in list
# variable contents
fp = open('recipes.txt')
contents = fp.readlines()

# sorting based on categorical variable meal class
contents.sort(key=my_sort)

# displaying contents on stdout after sorting
for line in contents:
    print(line)

fp.close()'''

# Executing the programme
def main():
    get_recipes()

main()
