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
import traceback

@login_required
def index(request, page_num=1):
    paginator = Paginator(Recipe.objects.all(), 10)

    page_num = max(1, min(page_num, paginator.num_pages)) #clamp in range [1, num_pages)
    recipes = [{"name": x.name, "description": f"Source: {x.source_name}" if x.source_name else "", "image": x.image_url, "id": x.id} for x in paginator.get_page(page_num)]
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
    query = request.GET.get("q", "")

    mode = request.GET.get("m", "1")
    if mode == "1":
        get_and_store_recipes_by_query(query=query, num=20, offset=(page_num-1)*20)
        paginator = Paginator(Recipe.objects.filter(name__contains=query).order_by("-added"), 10)
    else:
        paginator = Paginator(request.user.recipes.filter(name__contains=query).order_by("name"), 10)
    max_pages = paginator.num_pages

    page_num = max(1, min(page_num, max_pages)) #clamp in range [1, max_pages)
    recipes = [{"name": x.name, "description": f"Source: {x.source_name}" if x.source_name else "", "image": x.image_url, "id": x.id} for x in paginator.get_page(page_num)]
    return render(request, "recipewizard/recipes_view.html", {
        "title": "Search Results",
        "page": page_num,
        "max_pages": max_pages,
        "page_url": "search",
        "search_mode": mode,
        "recipes": recipes
    })

@login_required
def cookbook(request, page_num = 1):
    paginator = Paginator(request.user.recipes.all().order_by("-added"), 10)

    page_num = max(1, min(page_num, paginator.num_pages)) #clamp in range [1, num_pages)
    recipes = [{"name": x.name, "description": f"Source: {x.source_name}" if x.source_name else "", "image": x.image_url, "id": x.id} for x in paginator.get_page(page_num)]
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
    ingredients = [{"name": x.name, "amount": x.format_amount(), "unit": x.unit, "id": x.id} for x in request.user.shopping_list.all()]
    return render(request, "recipewizard/shopping_list.html", {
        "ingredients": ingredients,
        "allowed_units": supported_units
    })

@login_required
def batch_add_to_shopping_list(request):
    if request.method == "POST":
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)
        ingredients = json.loads(body["ingredients"])
        for ingredient_info in ingredients:
            ingredient = Ingredient()

            ingredient.amount = ingredient_info["amount"]
            ingredient.unit = ingredient_info["unit"]
            ingredient.name = ingredient_info["name"]

            try:
                ingredient.save()
            except Exception as e:
                print(e)
            else:
                request.user.shopping_list.add(ingredient)

        return JsonResponse({"success": True})

@login_required
def modify_shopping_list(request):
    if request.method == "POST":
        method = request.POST["_method"].upper()
        if method == "POST":
            ingredient = Ingredient()

            ingredient.amount = request.POST["amount"]
            ingredient.unit = request.POST["unit"]
            ingredient.name = request.POST["name"]

            try:
                ingredient.save()
            except Exception as e:
                messages.error(request, e)
            else:
                request.user.shopping_list.add(ingredient)
                messages.success(request, "Item successfully added.")
        elif method == "DELETE":
            toDelete = request.POST.getlist("toDelete")
            request.user.shopping_list.filter(id__in=toDelete).delete()
            messages.success(request, "Item(s) successfully deleted.")
    elif request.method == "PUT":
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)
        updates = body["updates"]
        
        ingredients_to_update = [x["ingredient"] for x in updates]
        ingredient_objs = request.user.shopping_list.filter(id__in=ingredients_to_update)

        for obj in ingredient_objs:
            table_entry = next((x for x in updates if int(x["ingredient"]) == obj.id), None)
            if table_entry:
                obj.amount = table_entry["value"]
                obj.save()
            
    return HttpResponseRedirect(reverse("shoppinglist"))

@login_required
def clear_shopping_list(request):
    if request.method == "POST":
        request.user.shopping_list.all().delete()
        messages.success(request, "Your shopping list has been cleared.")

    return HttpResponseRedirect(reverse("shoppinglist"))

@login_required
def kitchen(request):
    ingredients = [{"name": x.name, "amount": x.format_amount(), "unit": x.unit, "id": x.id} for x in request.user.ingredients.all()]
    return render(request, "recipewizard/my_kitchen.html", {
        "ingredients": ingredients,
        "allowed_units": supported_units
    })

@login_required
def modify_kitchen_ingredients(request):
    if request.method == "POST":
        method = request.POST["_method"].upper()
        if method == "POST":
            ingredient = Ingredient()

            ingredient.amount = request.POST["amount"]
            ingredient.unit = request.POST["unit"]
            ingredient.name = request.POST["name"]

            try:
                ingredient.save()
            except Exception as e:
                messages.error(request, e)
            else:
                request.user.ingredients.add(ingredient)
                messages.success(request, "Item successfully added.")
        elif method == "DELETE":
            toDelete = request.POST.getlist("toDelete")
            request.user.ingredients.filter(id__in=toDelete).delete()
            messages.success(request, "Item(s) successfully deleted.")
    elif request.method == "PUT":
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)
        updates = body["updates"]
        
        ingredients_to_update = [x["ingredient"] for x in updates]
        ingredient_objs = request.user.ingredients.filter(id__in=ingredients_to_update)

        for obj in ingredient_objs:
            table_entry = next((x for x in updates if int(x["ingredient"]) == obj.id), None)
            if table_entry:
                obj.amount = table_entry["value"]
                obj.save()
            
    return HttpResponseRedirect(reverse("kitchen"))

@login_required
def deduct_ingredients_from_kitchen(request):
    if request.method == "PUT":
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)
        ingredients_to_deduct = json.loads(body["ingredients"])

        try:
            for ingredient in ingredients_to_deduct:
                ingredients_in_kitchen = request.user.ingredients.filter(Q(name__iexact=ingredient["name"]) | Q(aliases__name__iexact=ingredient["name"])).iterator()
                
                amount_to_deduct = ingredient["amount"]
                deduct_unit = ingredient["unit"]
                deduct_name = ingredient["name"]
                
                next_ingredient = next(ingredients_in_kitchen, None)

                while amount_to_deduct > 0 and next_ingredient is not None:
                    next_ingredient_amount = next_ingredient.convert_amount_to_unit(deduct_unit)
                    if amount_to_deduct > next_ingredient_amount:
                        amount_to_deduct -= next_ingredient_amount
                        next_ingredient.deduct_amount(next_ingredient.name, next_ingredient.amount, next_ingredient.unit, 0.01)
                    else:
                        next_ingredient.deduct_amount(deduct_name, amount_to_deduct, deduct_unit, 0.01)
                        amount_to_deduct = 0

                    next_ingredient = next(ingredients_in_kitchen, None)
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": True})

@login_required
def add_ingredient_alias(request):
    if request.method == "POST":
        
        ingredient = request.user.ingredients.filter(id=request.POST["ingredient_id"]).first() #need to add a dropdown to the alias menu to choose an ingredient, this was an oversight
        alias_name = request.POST["alias"]

        if ingredient and alias_name:
            try:
                alias = Alias()
                alias.name = alias_name
                print(alias.name)
                alias.ingredient = ingredient
                alias.save()
            except Exception as e:
                print(e)
                messages.error(request, str(e))
            else:
                messages.success(request, "Alias successfully added.")

        
        return HttpResponseRedirect(reverse("recipe", kwargs={"recipe_id": request.POST["recipe_id"]}))    


@login_required
def recipe(request, recipe_id):
    try:
        recipe = Recipe.objects.filter(pk=recipe_id).first()
    except Recipe.DoesNotExist:
        return JsonResponse({"error": "No such recipe."}, status=404)

    ingredients = [{"amount_user_has": x.amount_of_ingredient_in_user_kitchen(request.user), "id": x.id, "name": x.name, "amount": x.format_amount(), "unit": x.unit} for x in recipe.ingredients.all()]

    source = ""

    if recipe.source_name is not None:
        source = f"Source: {recipe.source_name}"
    
    return render(request, "recipewizard/recipe_view.html", {
        "name": recipe.name,
        "description": source,
        "url": recipe.source_url,
        "image": recipe.image_url,
        "id": recipe.id,
        "saved": request.user.is_recipe_saved(recipe.id),
        "ingredients": ingredients,
        "servings": recipe.servings,
        "user_ingredients": request.user.ingredients.all()
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