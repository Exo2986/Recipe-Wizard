import json
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
            return render(request, "recipewizard/login.html", {
                "message": "Invalid username and/or password."
            })
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
            return render(request, "recipewizard/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "recipewizard/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "recipewizard/register.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def account(request):
    return render(request, "recipewizard/account.html")

def index(request):
    return render(request, "recipewizard/recipes_view.html", {
        "title": "All Recipes",
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

def recipe(request):
    return render(request, "recipewizard/recipe_view.html", {
        "ingredients": (
            {
                "name": "Milk",
                "amount": "2",
                "measurement": "Cups",
                "user_has_ingredient": True
            },
            {
                "name": "Flour",
                "amount": "8",
                "measurement": "Cups",
                "user_has_ingredient": True
            },
            {
                "name": "Eggs",
                "amount": "4",
                "measurement": "Large Eggs",
                "user_has_ingredient": False
            }
        )
    })