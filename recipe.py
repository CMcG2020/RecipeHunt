import requests

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
    mealType = input('Please chose a meal type: ')
    results = recipe_search(ingredient, time, mealType)
    print (results)

# find serving size for each recipe and calculate calories per serving

    
# make a file to store the results
    with open('recipes.txt', 'w') as file:
        for recipe in results:
            recipe_data = recipe['recipe']
            file.write('Recipe: ' + recipe_data['label'] + '\n')
            file.write('Calories: ' + str(recipe_data['calories']) + '\n')
            file.write('Time to cook: ' + str(recipe_data['totalTime']) + '\n')
            file.write('Ingredients: ' + str(recipe_data['ingredientLines']) + '\n')
            file.write('Link: ' + recipe_data['url'] + '\n')
            file.write('\n')
    file.close()
    return results

# function
def sort_recipes():
    with open('recipes.txt', 'r') as file:
        lines = file.readlines()
        lines.sort(key=lambda x: x.split()[1])
        file.close()
    with open('recipes.txt', 'w') as file:
        file.writelines(lines)
        file.close()

def display_recipes():
    with open('recipes.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            print(line)
        file.close()

def main():
    get_recipes()
    sort_recipes()
    display_recipes()

main()
