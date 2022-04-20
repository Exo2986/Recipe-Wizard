from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import IntegrityError
from fractions import Fraction

class User(AbstractUser):
    recipes = models.ManyToManyField("Recipe", related_name="+", blank=True)

    def is_recipe_saved(self, recipe_id):
        return self.recipes.filter(pk=recipe_id).exists()

class Recipe(models.Model):
    source_url = models.URLField(max_length=256)
    servings = models.IntegerField()
    api_id = models.IntegerField(unique=True)
    source_name = models.CharField(max_length=100, null=True)
    image_url = models.URLField(max_length=256, blank=True)
    name = models.CharField(max_length=100)
    added = models.DateField(auto_now_add=True)

    def from_json(recipe_json):
        try:
            recipe_obj = Recipe()

            recipe_obj.source_url = recipe_json["sourceUrl"]
            recipe_obj.servings = recipe_json["servings"]
            recipe_obj.image_url = recipe_json.get("image")
            recipe_obj.source_name = recipe_json["sourceName"]
            recipe_obj.api_id = recipe_json.get("id")
            recipe_obj.name = recipe_json["title"]

            recipe_obj.save()

            result = recipe_obj
        except IntegrityError as e: #If recipe is already in the database then don't store it again
            result = Recipe.objects.filter(api_id=recipe_json.get("id")).first()
        else:
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
                else:
                    recipe_obj.ingredients.add(ingredient_obj)

        return result

class Ingredient(models.Model):
    amount = models.DecimalField(decimal_places=3, max_digits=8)
    unit = models.CharField(max_length=32)
    name = models.CharField(max_length=64)
    api_id = models.IntegerField(blank=True, null=True)
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, related_name="ingredients", blank=True, null=True)
    shopping_list = models.ForeignKey("User", on_delete=models.CASCADE, related_name="shopping_list", blank=True, null=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="ingredients", blank=True, null=True)

    def format_amount(self):
        formatted = str(self.amount).strip("0") or "0"

        if formatted.startswith("."):
            formatted = "0" + formatted
        elif formatted.endswith("."):
            formatted = formatted[:-1]

        return formatted