"""recipewizard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("", views.index, name="index"),
    path("<int:page_num>", views.index, name="index-page"),
    path("search/<int:page_num>/", views.search, name="search"),
    path("recipe/<int:recipe_id>", views.recipe, name="recipe"),
    path("recipe/<int:recipe_id>/save", views.save_recipe, name="save_recipe"),
    path("kitchen/modify", views.modify_kitchen_ingredients, name="modify_kitchen_ingredients"),
    path("cookbook", views.cookbook, name="cookbook"),
    path("cookbook/<int:page_num>", views.cookbook, name="cookbook-page"),
    path("kitchen", views.kitchen, name="kitchen"),
    path("kitchen/batchdeduct", views.deduct_ingredients_from_kitchen, name="deduct_ingredients_from_kitchen"),
    path("kitchen/alias", views.add_ingredient_alias, name="add_ingredient_alias"),
    path("shoppinglist", views.shopping_list, name="shoppinglist"),
    path("shoppinglist/modify", views.modify_shopping_list, name="modify_shopping_list"),
    path("shoppinglist/clear", views.clear_shopping_list, name="clear_shopping_list"),
    path("shoppinglist/batchadd", views.batch_add_to_shopping_list, name="batch_add_to_shopping_list"),
    path("account", views.account, name="account")
]
