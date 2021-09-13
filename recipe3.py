import requests

EMPTY_ARGS = 'Api edamam.recipe-info needs some search query and none provided.'
EMPTY_CREDENTIALS = 'Check the Api Edamam recipe credentials.'

def get_recipe_info( recipe_name, app_id, app_key, max_results=5):
    """
    Get top results from the Edamam API for the passed recipe name.
    TODO force structure to this function
    :param recipe_app_id: Edamam recipe application id
    :param recipe_app_key: Edamam recipe application key
    :param recipe_name: Recipe name
    :param max_results: maximum number of results to be returned
    :return: top results
    """
    #app_id = 'f79ed4b2'
    #app_key = '758ec61e53ffcfdba764003d0c8ceb29'
    if recipe_name is None:
        raise ValueError(EMPTY_ARGS)
    if app_id is None or app_id == '' or app_key is None or app_key == '':
        raise ValueError(EMPTY_CREDENTIALS)

    connect_url = 'https://api.edamam.com/search?q={0}&app_id={1}&app_key={2}&from=0&to={3}'
    url = connect_url.format(recipe_name, app_id, app_key, max_results)
    
    response_obj = requests.get(url)

    recipes_info = []
    if response_obj:
        response_text = response_obj.json()['hits']

        recipe_columns = ['source', 'url', 'ingredientLines', 'cautions', 'healthLabels', 'calories', 'image']

        for response in response_text:
            recipe = response['recipe']
            recipe_info = dict()
            recipe_info['label'] = recipe['label']

            for recipe_col in recipe_columns:
                recipe_info[recipe_col] = recipe[recipe_col]
            recipes_info.append(recipe_info)
    else:
        print('No recipe found for the search query')

    return recipes_info

def get_recipes():
    app_id = input("Enter app_id")
    app_key = input("Enter app_key")
    
    ingredient = input('Enter an ingredient: ')
    #time = input('How much time do you have to cook: ')
    #mealType = input('Please chose a meal type: Breakfast, Dinner, Lunch, Snack, Teatime: ')
    print(get_recipe_info(ingredient))

get_recipes()