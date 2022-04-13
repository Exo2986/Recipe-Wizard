import json
from .api_manager import *
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

api = APIManager()

api.get_and_store_random_recipes(10)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, "recipewizard/login.html")
    else:
        return render(request, "recipewizard/login.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.error(request, "Passwords must match.")
            return render(request, "recipewizard/register.html")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.error(request, "Username already taken.")
            return render(request, "recipewizard/register.html")
        login(request, user)
        messages.success(request, "Your account has been created.")
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "recipewizard/register.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@login_required
def account(request):
    return render(request, "recipewizard/account.html")

@login_required
def index(request):
    recipes = [{"name": x.name, "description": f"Source: {x.source_name}", "image": x.image_url, "id": x.id} for x in Recipe.objects.order_by('?')[:10]]
    return render(request, "recipewizard/recipes_view.html", {
        "title": "All Recipes",
        "recipes": recipes
    })

@login_required
def cookbook(request):
    return render(request, "recipewizard/recipes_view.html", {
        "title": "My Cookbook",
        "recipes": (
            {
                "name": "Test1",
                "description": "This is a test.",
                "image": "https://www.simplyrecipes.com/thmb/mbN8mXZ0srgAT1YrDU61183t0uM=/648x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/Simply-Recipes-Homemade-Pizza-Dough-Lead-Shot-1b-ea13798d224048b3a28afb0936c9b645.jpg"     
            }, 
            {
                "name": "Test2",
                "description": "This is a test.",
                "image": "https://images.immediate.co.uk/production/volatile/sites/30/2013/05/Puttanesca-fd5810c.jpg?quality=90&webp=true&resize=300,272"     
            }, 
            {
                "name": "Test2",
                "description": "This is a test.",
                "image": "https://images.immediate.co.uk/production/volatile/sites/30/2021/03/Cacio-e-Pepe-e44b9f8.jpg?quality=90&webp=true&resize=300,272"     
            }
        )
    })

@login_required
def shopping_list(request):
    messages.success(request, "Changes have been saved.")
    return render(request, "recipewizard/shopping_list.html", {
        "ingredients": (
            {
                "name": "Milk",
                "amount": "1",
                "measurement": "Cups"
            },
            {
                "name": "Flour",
                "amount": "4",
                "measurement": "Cups"
            },
            {
                "name": "Butter",
                "amount": "2",
                "measurement": "Stick"
            }
        )
    })

@login_required
def kitchen(request):
    return render(request, "recipewizard/my_kitchen.html", {
        "ingredients": (
            {
                "name": "Milk",
                "amount": "1",
                "measurement": "Cups"
            },
            {
                "name": "Flour",
                "amount": "4",
                "measurement": "Cups"
            },
            {
                "name": "Butter",
                "amount": "2",
                "measurement": "Stick"
            }
        )
    })

@login_required
def recipe(request, recipe_id):
    try:
        recipe = Recipe.objects.filter(pk=recipe_id).first()
    except Recipe.DoesNotExist:
        return JsonResponse({"error": "No such recipe."}, status=404)

    ingredients = [{"user_has_ingredient": True, "name": x.name, "amount": x.amount, "unit": x.unit} for x in recipe.ingredients.all()]

    return render(request, "recipewizard/recipe_view.html", {
        "name": recipe.name,
        "description": f"Source: {recipe.source_name}",
        "url": recipe.source_url,
        "image": recipe.image_url,
        "ingredients": ingredients
    })