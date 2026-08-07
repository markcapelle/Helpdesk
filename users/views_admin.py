from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import AdminUserCreateForm, AdminProfileForm
from .utils import admin_required

@admin_required
def admin_user_list(request):
    users = User.objects.all().order_by("username")
    return render(request, "users/admin/user_list.html", {"users": users})


@admin_required
def admin_create_user(request):
    if request.method == "POST":
        user_form = AdminUserCreateForm(request.POST)
        profile_form = AdminProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data["password1"])
            user.save()

            profile = user.profile
            profile.country_code = profile_form.cleaned_data["country_code"]
            profile.phone = profile_form.cleaned_data["phone"]
            profile.avatar = profile_form.cleaned_data["avatar"]
            profile.role = profile_form.cleaned_data["role"]
            profile.save()

            messages.success(request, "User created successfully.")
            return redirect("admin_user_list")
    else:
        user_form = AdminUserCreateForm()
        profile_form = AdminProfileForm()

    return render(request, "users/admin/user_form.html", {
        "title": "Create User",
        "submit_label": "Create",
        "user_form": user_form,
        "profile_form": profile_form,
    })


@admin_required
def admin_reset_password(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        new_password = request.POST.get("password")
        user.set_password(new_password)
        user.save()
        messages.success(request, "Password reset successfully.")
        return redirect("admin_user_list")

    return render(request, "users/admin/reset_password.html", {"user": user})
