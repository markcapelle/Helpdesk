from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import AdminUserCreateForm, AdminProfileForm, AdminUserEditForm
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

    return render(request, "users/admin/new_user.html", {
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
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("admin_reset_password", user_id=user_id)

        user.set_password(new_password)
        user.save()

        messages.success(request, "Password reset successfully.")
        return redirect("admin_user_list")

    return render(request, "users/admin/reset_password.html", {"user": user})



@admin_required
def admin_edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = user.profile

    if request.method == "POST":
        user_form = AdminUserEditForm(request.POST, instance=user)
        profile_form = AdminProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "User updated successfully.")
            return redirect("admin_user_list")

    else:
        user_form = AdminUserEditForm(instance=user)
        profile_form = AdminProfileForm(instance=profile)

    return render(request, "users/admin/user_form.html", {
        "title": f"Edit User: {user.username}",
        "submit_label": "Save Changes",
        "user_form": user_form,
        "profile_form": profile_form,
    })



@admin_required
def admin_delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        # Delete profile first (safe)
        if hasattr(user, "profile"):
            user.profile.delete()

        # Delete user
        user.delete()

        messages.success(request, "User deleted successfully.")
        return redirect("admin_user_list")

    return redirect("admin_user_list")


@admin_required
def admin_view_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = user.profile
    return render(request, "users/view_profile.html", {
        "user": user,
        "profile": profile,
        "admin_view": True,   # flag so template knows this is admin mode
    })
