from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    recipes = models.ManyToManyField("Recipe", related_name="+", blank=True)
    shopping_list = models.ForeignKey("ShoppingList", on_delete=models.CASCADE, blank=True, null=True)

class Recipe(models.Model):
    source_url = models.URLField(max_length=256)
    servings = models.IntegerField()
    api_id = models.IntegerField(unique=True)
    source_name = models.CharField(max_length=100)
    image_url = models.URLField(max_length=256, blank=True)
    name = models.CharField(max_length=100)

class Ingredient(models.Model):
    amount = models.IntegerField()
    unit = models.CharField(max_length=32)
    name = models.CharField(max_length=64)
    api_id = models.IntegerField()
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, related_name="ingredients", blank=True, null=True)
    shopping_list = models.ForeignKey("ShoppingList", on_delete=models.CASCADE, related_name="ingredients", blank=True, null=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="ingredients", blank=True, null=True)

class ShoppingList(models.Model):
    pass