import requests
from . import constants
from . import models
from django.db import IntegrityError
import json

def get_and_store_random_recipes(num):
    response = requests.get("https://api.spoonacular.com/recipes/random",\
        params={"number": num},\
        headers={"X-Api-Key": constants.NUTRITION_API_KEY})

    js = response.json()

    for recipe_json in js["recipes"]:
        models.Recipe.from_json(recipe_json)

def get_and_store_recipes_by_query(query, num, offset):
    offset = max(0, min(900, offset)) #clamp between 0 and 900
    params={"number": num, "query": query, "offset": offset, "fillIngredients": True, "addRecipeInformation": True, "sort": "popularity"}

    response = requests.get("https://api.spoonacular.com/recipes/complexSearch",\
        params=params,\
        headers={"X-Api-Key": constants.NUTRITION_API_KEY})

    js = response.json()

    results = list()

    for recipe_json in js["results"]:
        result = models.Recipe.from_json(recipe_json)
        if result is not None:
            results.append(result)

    return results

def convert_units(ingredient, target_unit):
    params = {"ingredientName": ingredient.name, "sourceAmount": ingredient.amount, "sourceUnit": ingredient.unit, "targetUnit": target_unit}

    response = requests.get("https://api.spoonacular.com/recipes/convert",\
        params=params,\
        headers={"X-Api-Key": constants.NUTRITION_API_KEY})

    js = response.json()

    print(js)

    return js["targetAmount"]