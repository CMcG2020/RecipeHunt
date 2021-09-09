import requests

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

   
    ingredient = input('Enter an ingredient: ')
    time = input('How much time do you have to cook: ')

    results = recipe_search(ingredient, time)
    #print (results)
    

    with open('recipes.txt', 'w') as file:
        for result in results:
            recipe = result['recipe']
            #print("Label:- ", recipe['label'])
            file.write(recipe['label']+ '\n')
            print("url:- ",recipe['url'])
            #file.write(recipe['url'] + '\n')
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
