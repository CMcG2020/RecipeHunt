
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
    mealType = input('Please chose a meal type: Breakfast, Dinner, Lunch, Snack, Teatime: ')
    results = recipe_search(ingredient, time, mealType)
    print (results)

   
# make a file to store the results
    with open('recipes.txt', 'w') as file:
        for recipe in results:
            recipe_data = recipe['recipe']
            # find serving size for each recipe and calculate calories per serving
            calories_per_serving = int(recipe_data['calories'] / int(recipe_data['yield']))
            file.write('Recipe: ' + recipe_data['label'] + '\n')
            file.write('Calories: ' + str(recipe_data['calories']) + '\n')
            file.write('Calories per serving: ' + str(calories_per_serving) + '\n')
            file.write('Time to cook: ' + str(recipe_data['totalTime']) + '\n')
            file.write('Ingredients: ' + str(recipe_data['ingredientLines']) + '\n')
            file.write('Link: ' + recipe_data['url'] + '\n')
            file.write('\n')
    file.close()
    return results

 def write_to_csv(self, results):
            with open('recipe.csv', 'w') as csvfile:
                fieldnames = ['recipe_name', 'yield', 'calories_per_serving', 'recipe_url', 'ingredients']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for recipe in results:
                    writer.writerow(recipe)

# function to sort by calories per serving
def read_file(file_name):
    with open(file_name) as f:
        lines = f.readlines()
        return lines

def sort_file(file_name):
    lines = read_file(file_name)
    lines.sort(key=lambda line: line.split()[2])
    return lines

def print_sorted_file(file_name):
    lines = sort_file(file_name)
    for line in lines:
        print(line)

# sort the file and display the top 5 results by calories
def sort_file():
    df = pd.read_csv('recipe.csv', encoding='unicode_escape')
    df = df.sort_values(by=['calories_per_serving'], ascending=True)
    df.to_csv('recipe.csv', index=False)


def display_top_5():
    df = pd.read_csv('recipe.csv', encoding='unicode_escape')
    print(df.head(5))


def main():
    get_recipes()
    print_sorted_file("recipes.txt")

main()
