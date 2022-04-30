from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import IntegrityError
from fractions import Fraction
from django.db.models import Q
from datetime import datetime, timedelta, timezone
from . import api_manager
import decimal

class User(AbstractUser):
    recipes = models.ManyToManyField("Recipe", related_name="+", blank=True)
    failed_login_attempts = models.PositiveSmallIntegerField(default=0)
    last_failed_login_attempt = models.DateTimeField(blank=True, null=True)
    account_unlock_datetime = models.DateTimeField(blank=True, null=True)

    def is_account_locked(self):
        if self.account_unlock_datetime is not None:
            now = datetime.now(tz=timezone(timedelta()))
            if now < self.account_unlock_datetime:
                return True
            else:
                self.account_unlock_datetime = None
                self.failed_login_attempts = 0
                self.save()
        return False

    def increment_failed_login_attempts(self):
        if self.last_failed_login_attempt is not None and datetime.now(tz=timezone(timedelta())) - self.last_failed_login_attempt >= timedelta(minutes=3):
            self.failed_login_attempts = 0
        
        self.failed_login_attempts+=1
        self.last_failed_login_attempt = datetime.now(tz=timezone(timedelta()))

        if self.failed_login_attempts >= 3:
            self.account_unlock_datetime = datetime.now(tz=timezone(timedelta())) + timedelta(minutes=5)

        self.save()

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


supported_units = ["gallon", "teaspoon", "tablespoon", "fluid ounce", "cup", "pint", "quart", "milliliter", "liter", "pound", "ounce", "milligram", "gram", "kilogram", "piece"]
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

    def convert_amount_to_unit(self, target_unit):
        return api_manager.convert_units_from_ingredient(self, target_unit)

    def user_has_ingredient(self, user):
        return self.amount_of_ingredient_in_user_kitchen(user) >= self.amount

    def amount_of_ingredient_in_user_kitchen(self, user):
        test = user.ingredients.all()
        for i in test:
            print(self.name, " " , i.aliases.count())

        matching_ingredients = user.ingredients.filter(Q(name__iexact=self.name) | Q(aliases__name__iexact=self.name)).all()

        total_amount = 0

        for ingredient in matching_ingredients:
            total_amount += ingredient.convert_amount_to_unit(self.unit)

        return total_amount

    def deduct_amount(self, name, amount, unit, tolerance):
        if unit != self.unit:
            amount = decimal.Decimal(api_manager.convert_units(name, amount, unit, self.unit))
            
        self.amount -= amount

        if (self.amount < tolerance):
            self.delete()
        else:
            self.save()

class Alias(models.Model):
    name = models.CharField(max_length=64)
    ingredient = models.ForeignKey("Ingredient", on_delete=models.CASCADE, related_name="aliases", blank=True, null=True)
