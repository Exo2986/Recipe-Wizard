from django.urls import path
from . import views

urlpatterns = [
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("account", views.account, name="account"),
    path("account/update", views.account_update, name="account_update"),
]
