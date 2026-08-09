from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm, UserSelfServiceForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

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


# Login required to view dashboard
@login_required
def dashboard(request):
    return render(request, "dashboard.html")


# Edit user profile
@login_required
def edit_user(request):
    user = request.user

    if request.method == "POST":
        user_form = UserSelfServiceForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user.profile)


        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated.")
            return redirect("dashboard")
    else:
        user_form = UserSelfServiceForm(instance=user)
        profile_form = UserProfileForm(instance=user.profile)

    return render(request, "users/user_form.html", {
        "title": "Edit Your Profile",
        "submit_label": "Save Changes",
        "user_form": user_form,
        "profile_form": profile_form,
    })


@login_required
def user_reset_password(request):
    user = request.user

    if request.method == "POST":
        new_password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("user_reset_password")

        try:
            validate_password(new_password, user=user)
        except ValidationError as e:
            for msg in e.messages:
                messages.error(request, msg)
            return redirect("user_reset_password")

        user.set_password(new_password)
        user.save()

        messages.success(request, "Password reset successfully. Please log in again.")
        return redirect("login")

    return render(request, "users/reset_password.html")


@login_required
def view_profile(request):
    user = request.user
    profile = user.profile
    return render(request, "users/view_profile.html", {
        "user": user,
        "profile": profile,
    })


# Logout view
def logout_page(request):
    logout(request)
    return redirect("homepage")
