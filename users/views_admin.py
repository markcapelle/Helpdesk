from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import AdminUserCreateForm, AdminProfileForm, AdminUserEditForm
from .utils import admin_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

#-----------------------------
# Manage user list - as admin
#-----------------------------
@admin_required
def admin_user_list(request):
    users = User.objects.all().order_by("username")

    # Hide superusers unless the viewer is a superuser
    if not request.user.is_superuser:
        users = users.filter(is_superuser=False)

    return render(request, "users/admin/user_list.html", {"users": users})


#-----------------------------
# Create user - as admin
#-----------------------------
@admin_required
def admin_create_user(request):
    if request.method == "POST":
        user_form = AdminUserCreateForm(request.POST)
        profile_form = AdminProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data["password1"])
            user.save()

            group = profile_form.cleaned_data["role"]
            if group:
                user.groups.add(group)

            profile = user.profile
            profile.country_code = profile_form.cleaned_data["country_code"]
            profile.phone = profile_form.cleaned_data["phone"]
            profile.avatar = profile_form.cleaned_data["avatar"]
            profile.role = profile_form.cleaned_data["role"]
            profile.save()

            return redirect("admin_user_list")

        return render(request, "users/admin/new_user.html", {
            "title": "Create User",
            "submit_label": "Create",
            "user_form": user_form,
            "profile_form": profile_form,
        })

    else:
        user_form = AdminUserCreateForm()
        profile_form = AdminProfileForm()

    return render(request, "users/admin/new_user.html", {
        "title": "Create User",
        "submit_label": "Create",
        "user_form": user_form,
        "profile_form": profile_form,
    })



#-----------------------------
# Reset user password - as admin
#-----------------------------
@admin_required
def admin_reset_password(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        new_password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("admin_reset_password", user_id=user_id)

        try:
            validate_password(new_password, user=user)
        except ValidationError as e:
            for msg in e.messages:
                messages.error(request, msg)
            return redirect("admin_reset_password", user_id=user_id)

        user.set_password(new_password)
        user.save()

        return redirect("admin_user_list")

    return render(request, "users/admin/reset_password.html", {"user": user})


#-----------------------------
# Edit user - as admin
#-----------------------------
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
            group = profile_form.cleaned_data["role"]
            user.groups.clear()
            if group:
                user.groups.add(group)
            messages.success(request, "User updated successfully.")
            return render(request, "users/admin/user_form.html", {
                "title": f"Edit User: {user.username}",
                "submit_label": "Save Changes",
                "user_form": user_form,
                "profile_form": profile_form,
            })


    else:
        user_form = AdminUserEditForm(instance=user)
        profile_form = AdminProfileForm(instance=profile)

    return render(request, "users/admin/user_form.html", {
        "title": f"Edit User: {user.username}",
        "submit_label": "Save Changes",
        "user_form": user_form,
        "profile_form": profile_form,
    })



#-----------------------------
# Delete user - as admin
#-----------------------------
@admin_required
def admin_delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        # Delete profile first (safe)
        if hasattr(user, "profile"):
            user.profile.delete()

        # Delete user
        user.delete()

        return redirect("admin_user_list")

    return redirect("admin_user_list")



#-----------------------------
# View user - as admin
#-----------------------------
@admin_required
def admin_view_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = user.profile
    return render(request, "users/view_profile.html", {
        "user": user,
        "profile": profile,
        "admin_view": True,   # flag so template knows this is admin mode
    })
