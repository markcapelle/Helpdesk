from django.urls import path
from django.shortcuts import render

# Temporary simple render views until you build full logic
def login_page(request):
    return render(request, "login.html")

def register_page(request):
    return render(request, "register.html")

urlpatterns = [
    path("login/", login_page, name="login"),
    path("register/", register_page, name="register"),
]
