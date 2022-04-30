import json
from recipewizard.api_manager import *
from recipewizard.models import *
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

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user_obj = User.objects.filter(username=username).first()
        if user_obj is not None and user_obj.is_account_locked(): #dont authenticate
            messages.error(request, "This account is locked due to too many failed login attempts. Please try again later.")
            return render(request, "account/login.html")
        else: #try authentication
            user = authenticate(request, username=username, password=password)

            # Check if authentication successful
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                if user_obj is not None:
                    user_obj.increment_failed_login_attempts()
                messages.error(request, "Invalid username or password.")
                return render(request, "account/login.html")
    else:
        return render(request, "account/login.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.error(request, "Passwords must match.")
            return render(request, "account/register.html")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.error(request, "Username already taken.")
            return render(request, "account/register.html")
        login(request, user)
        messages.success(request, "Your account has been created.")
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "account/register.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@login_required
def account(request):
    return render(request, "account/account.html")

@login_required
def account_update(request):
    if request.method == "POST":
        password = request.POST.get("password", False)
        username = request.POST.get("username", False)
        email = request.POST.get("email", False)

        if password:
            old_password = request.POST.get("oldPassword", False)
            password_confirm = request.POST.get("passwordConfirm", False)

            password_check = request.user.check_password(old_password)

            if password_check and password == password_confirm:
                try:
                    request.user.set_password(password)
                    request.user.save()

                    messages.success(request, "Your password has been updated.")
                except Exception as e:
                    messages.error(request, str(e))
            elif not password_check:
                messages.error(request, "Incorrect password.")
            elif password != password_confirm:
                messages.error(request, "Passwords must match.")
        elif username:
            try:
                request.user.username = username
                request.user.save()
            except Exception as e:
                messages.error(request, str(e))
        elif email:
            old_email = request.POST.get("oldEmail", False)
            email_confirm = request.POST.get("emailConfirm", False)
            if request.user.email == old_email and email == email_confirm:
                try:
                    request.user.email = email
                    request.user.save()

                    messages.success(request, "Your email has been updated.")
                except Exception as e:
                    messages.error(request, str(e))
            elif request.user.email != old_email:
                messages.error(request, "Current email is incorrect.")
            elif email != email_confirm:
                messages.error(request, "Emails must match.")

        return HttpResponseRedirect(reverse("account"))