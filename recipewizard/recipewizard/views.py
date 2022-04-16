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

#api.get_and_store_random_recipes(30)

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
def index(request, page_num=1):
    paginator = Paginator(Recipe.objects.all(), 10)

    page_num = max(1, min(page_num, paginator.num_pages-1)) #clamp in range [1, num_pages)
    recipes = [{"name": x.name, "description": f"Source: {x.source_name}", "image": x.image_url, "id": x.id} for x in paginator.get_page(page_num)]
    return render(request, "recipewizard/recipes_view.html", {
        "title": "All Recipes",
        "page": page_num,
        "max_pages": paginator.num_pages,
        "page_url": "index-page",
        "search_mode": 1,
        "recipes": recipes
    })
    
@login_required
def search(request, page_num):
    mode = request.GET.get("m", "1")
    if mode == "1":
        paginator = Paginator(Recipe.objects.filter(name__contains=request.GET.get("q", "")), 10)
    else:
        paginator = Paginator(request.user.recipes.filter(name__contains=request.GET.get("q", "")), 10)

    page_num = max(1, min(page_num, paginator.num_pages-1)) #clamp in range [1, num_pages)
    recipes = [{"name": x.name, "description": f"Source: {x.source_name}", "image": x.image_url, "id": x.id} for x in paginator.get_page(page_num)]
    return render(request, "recipewizard/recipes_view.html", {
        "title": "Search Results",
        "page": page_num,
        "max_pages": paginator.num_pages,
        "page_url": "search",
        "search_mode": mode,
        "recipes": recipes
    })

@login_required
def cookbook(request, page_num = 1):
    paginator = Paginator(request.user.recipes.all(), 10)

    print(paginator.num_pages)

    page_num = max(1, min(page_num, paginator.num_pages)) #clamp in range [1, num_pages)
    recipes = [{"name": x.name, "description": f"Source: {x.source_name}", "image": x.image_url, "id": x.id} for x in paginator.get_page(page_num)]
    return render(request, "recipewizard/recipes_view.html", {
        "title": "My Cookbook",
        "page": page_num,
        "max_pages": paginator.num_pages,
        "page_url": "cookbook-page",
        "search_mode": 2,
        "recipes": recipes
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

    ingredients = [{"user_has_ingredient": True, "name": x.name, "amount": x.format_amount(), "unit": x.unit} for x in recipe.ingredients.all()]

    return render(request, "recipewizard/recipe_view.html", {
        "name": recipe.name,
        "description": f"Source: {recipe.source_name}",
        "url": recipe.source_url,
        "image": recipe.image_url,
        "id": recipe.id,
        "saved": request.user.is_recipe_saved(recipe.id),
        "ingredients": ingredients
    })

@csrf_exempt
@login_required
def save_recipe(request, recipe_id):
    if request.method == "PUT":
        try:
            recipe = Recipe.objects.filter(pk=recipe_id).first()
        except Exception:
            return JsonResponse({"error": "Recipe not found."}, status=404)
        else:
            saved = request.user.is_recipe_saved(recipe_id)
            if saved:
                request.user.recipes.remove(recipe)
            else:
                request.user.recipes.add(recipe)

            return JsonResponse({"saved": not saved})