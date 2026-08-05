from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Login request
def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

# Register page
def register_page(request):
    return render(request, "register.html")

# Login required to view dashboard
@login_required
def dashboard(request):
    return render(request, "dashboard.html")

# Logout view
def logout_page(request):
    logout(request)
    return redirect("homepage")