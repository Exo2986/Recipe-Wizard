import requests
from . import constants
from .models import *
from django.db import IntegrityError
import json

class APIManager():
    def get_and_store_random_recipes(self, num):
        response = requests.get("https://api.spoonacular.com/recipes/random",\
            params={"number": num},\
            headers={"X-Api-Key": constants.NUTRITION_API_KEY})

        js = response.json()

        for recipe_json in js["recipes"]:
            try:
                recipe_obj = Recipe()

                recipe_obj.source_url = recipe_json["sourceUrl"]
                recipe_obj.servings = recipe_json["servings"]
                recipe_obj.image_url = recipe_json.get("image")
                recipe_obj.source_name = recipe_json["sourceName"]
                recipe_obj.api_id = recipe_json.get("id")
                recipe_obj.name = recipe_json["title"]

                recipe_obj.save()
            except IntegrityError: #If recipe is already in the database then don't store it again
                continue

            for ingredient_json in recipe_json["extendedIngredients"]:
                ingredient_obj = Ingredient()

                ingredient_obj.amount = ingredient_json["amount"]
                ingredient_obj.unit = ingredient_json["unit"]
                ingredient_obj.name = ingredient_json["name"]
                ingredient_obj.api_id = ingredient_json["id"]

                try:
                    ingredient_obj.save()
                except Exception:
                    pass
                finally:
                    recipe_obj.ingredients.add(ingredient_obj)