from spellchecker import SpellChecker
import requests
import json
import webbrowser
from sys import exit


# create a function that makes a request to the Edamam API with the required ingredient
def list_recipes(user_ingredient, user_dishtype, user_cook_time):
    app_id = "d8f723ac"
    app_key = "6d5990eea37ae2bec55fefe5ee06522c"
    url = f"https://api.edamam.com/api/recipes/v2?type=public&q={user_ingredient}&app_id={app_id}&app_key={app_key}{user_dishtype}{user_cook_time}"
    response = requests.get(url)
    recipes = response.json()

    # print(url)
    return recipes["hits"]


def search_recipes():
    def spellcheck_user_ingredient(user_input_ingredient):

        # spell checker
        spell = SpellChecker(language=None, case_sensitive=False)

        # load spellcheck file
        spell.word_frequency.load_text_file('C:/Users/tvasa/Desktop/PYTHON FILES/Ingredients_List.txt')

        # variables
        correct_ingredient = user_input_ingredient == spell.correction(user_input_ingredient)
        correction = spell.correction(user_input_ingredient)

        # if you overwhelm the spell correction then it just puts it as a true condition anyway
        if correct_ingredient:
            print(f"{user_input_ingredient} is a great choice! Please bear with me while I take a look for you :)")
            user_input_ingredient == correct_ingredient

        elif not correct_ingredient:
            suggestion = input(f"You wrote {user_input_ingredient}. Did you mean {correction}? Y/N").upper()

            if suggestion == "Y":
                user_input_ingredient == correction

            elif suggestion == "N":
                user_input_ingredient_check = input("What ingredient would you like your recipe to be based on? ")
                spellcheck_user_ingredient(user_input_ingredient_check)

            else:
                print("Error - spellcheck user ingredient")
                user_input_ingredient_check = input("What ingredient would you like your recipe to be based on? ")
                spellcheck_user_ingredient(user_input_ingredient_check)

        else:
            print("Errors!")
            user_input_ingredient_check = input("What ingredient would you like your recipe to be based on? ")
            spellcheck_user_ingredient(user_input_ingredient_check)

        return user_input_ingredient

    user_input_ingredient = input("What ingredient would you like your recipe to be based on? ")

    user_ingredient = spellcheck_user_ingredient(user_input_ingredient)

    # ask the user to enter the ingredient they want to search for
    # user_ingredient = input("What ingredient do you want to include? ")

    # check dishtype
    def check_dishtype(input_dishtype):
        # check for typo?
        if input_dishtype == "starter":
            dishtype = "&dishType=Starter"
        elif input_dishtype == "main":
            dishtype = "&dishType=Main%20course"
        elif input_dishtype == "side dish":
            dishtype = "&dishType=Side%20dish"
        elif input_dishtype == "dessert":
            dishtype = "&dishType=Desserts"
        else:
            print("Error! Please enter a dishtype.")
            # write break condition
            input_dishtype_check = input("Is it a Starter, Side Dish, Main or Dessert?").lower()
            check_dishtype(input_dishtype_check)

        return dishtype

    # ask the user for dishtype
    input_dishtype = input("Is it a Starter, Side Dish, Main or Dessert?").lower()
    user_dishtype = check_dishtype(input_dishtype)

    # check cook time
    def check_cook_time(input_cook_time):
        # check for typo?
        if input_cook_time.isdigit():
            cook_time = f"&time={input_cook_time}"

        else:
            print("Error! Please enter your maximum cooking time.")
            # check cook time again
            input_cook_time_check = input(
                "How much time do you have to cook? Please enter maximum time in minutes e.g. '30'. ")
            check_cook_time(input_cook_time_check)

        return cook_time

    # ask user for cook time input
    input_cook_time = input("How much time do you have to cook? Please enter maximum time in minutes e.g. '30'. ")
    user_cook_time = check_cook_time(input_cook_time)

    # create a dictionary of search results
    recipe_dict = {}
    count = 0

    # get the returned recipes from the API response
    results = list_recipes(user_ingredient, user_dishtype, user_cook_time)

    # display the recipes for each search result
    for result in results:
        recipe = result["recipe"]
        recipe_label = recipe["label"]
        recipe_url = recipe["url"]
        count = count + 1
        recipe_dict[count] = recipe_url

        print(f"{count}. ", recipe_label)
        print("")

    # check dictionary results function
    def check_len_results(recipe_dict):

        len_dict = len(recipe_dict)

        if len_dict <= 0:
            print("Sorry, your search produced no results.")

            # check if user wants to make a new search
            user_repeat_search = input("Do you want to make a new search for recipes? Y/N").upper()

            # call new search from parent function
            if user_repeat_search == "Y":
                search_recipes()

            elif user_repeat_search == "N":
                print("Complete - user repeat search")
                sys.exit()

            else:
                print("Error - user repeat search")
                # send to repeat search loop
                check_user_repeat_search = input("Do you want to make a new search for recipes? Y/N").upper()
                repeat_search(check_user_repeat_search)

                # call function to check on dictionary results

    check_len_results(recipe_dict)

    # function loop to check if user wants to select recipe url to open
    def select_recipe(user_select_recipe, recipe_dict):

        if user_select_recipe.isdigit():
            recipe_key = int(user_select_recipe)
            recipe_val = recipe_dict.get(recipe_key)
            webpage = webbrowser.open_new(f"{recipe_val}")

            # function loop to check if user wants to select recipe url to open another url
            def select_again_url(recipe_dict):
                # select another recipe?
                select_again = input("Do you want to open another recipe url? Y/N").upper()

                # if yes repeat function
                if select_again == "Y":
                    user_select_recipe = input("Enter the recipe number e.g.'5' to open the recipe url: ")
                    select_recipe(user_select_recipe, recipe_dict)

                # message completion
                elif select_again == "N":
                    print("Complete - url selection")
                    # do you want to make a new search - yes - no
                    check_user_repeat_search = input("Do you want to make a new search for recipes? Y/N").upper()
                    repeat_search(check_user_repeat_search)

                # message error repeat function
                else:
                    print("Error - user input select another url.")
                    # write new condition
                    # here it is looping to search for new recipe?
                    select_again_url(recipe_dict)

            # call select again url function - user choice open another url
            select_again_url(recipe_dict)

        else:
            print("Error - user input URL.")
            user_select_recipe = input("Enter the recipe number e.g.'5' to open the recipe url: ")
            select_recipe(user_select_recipe, recipe_dict)

    # user select recipe to open url
    user_select_recipe = input("Enter the recipe number e.g.'5' to open the recipe url: ")

    select_recipe = select_recipe(user_select_recipe, recipe_dict)

    # do you want to make a new search - yes - no
    user_repeat_search = input("Do you want to make a new search for recipes? Y/N").upper()

    repeat_search(user_repeat_search)


# function loop to check if user wants to repeat search
def repeat_search(user_repeat_search):
    if user_repeat_search == "Y":
        search_recipes()

    elif user_repeat_search == "N":
        print("Complete - recipe search")
        sys.exit()

    else:
        print("Error - user input new recipe search")
        # check input
        user_repeat_search = input("Do you want to make a new search for recipes? Y/N").upper()
        repeat_search(user_repeat_search)


search_recipes()