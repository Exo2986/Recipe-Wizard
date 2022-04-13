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
            Recipe.from_json(recipe_json)