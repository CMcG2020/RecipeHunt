import requests
import os.path

def recipe_search(ingredient, time):
    # Register to get an APP ID and key https://developer.edamam.com/
    app_id = 'f79ed4b2'
    app_key = '758ec61e53ffcfdba764003d0c8ceb29'
    result = requests.get(
    'https://api.edamam.com/search?q={}&app_id={}&app_key={}&time={}'
    .format(ingredient, app_id,app_key, time))
    data = result.json()
    return data['hits']

def get_recepies():

    while True:
        try:
            ingredient = input('Enter an ingredient: ')
            if ingredient.isdigit():
                raise ValueError
            else:
                time = input('How much time do you have to cook: ')
        except ValueError:
                print("Please enter ingredient name")

    time = input('How much time do you have to cook: ')
    results = recipe_search(ingredient, time)
    #print (results)
    
    file_path = r'C:\Users\goatl\Desktop'
    file_name = 'recipes.txt'
    with open(os.path.join(file_path, file_name, 'w')) as file:
        for result in results:
            recipe = result['recipe']
            print("Label:- ", recipe['label'])
            file.write(recipe['label'] + '\n')
            print("uri:- ",recipe['uri'])
            print("url:- ",recipe['url'])
            print("ingridentlines:- ", recipe['ingredientLines'])
            print("mealtype:- ", recipe['mealType'])
            print("dietlabels:- ", recipe['dietLabels'])
            print("healthlabels:- ", recipe['healthLabels'])
            print("ingridients:- ", recipe['ingredients'])
            print("calories:- ", recipe['calories'])
            print("serving:- ", recipe['yield'])
            print("totaltime:- ", recipe['totalTime'])
            print("cuisine:- ", recipe['cuisineType'])
            print("nutrients:- ", recipe['totalNutrients'])
            print()
            file.close()
            
        

get_recepies()
