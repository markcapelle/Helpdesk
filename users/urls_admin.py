from django.urls import path
from .views_admin import (
    admin_user_list,
    admin_create_user,
    admin_delete_user,
    admin_edit_user,
    admin_reset_password,
    admin_view_profile,
)

urlpatterns = [
    path("users/", admin_user_list, name="admin_user_list"),
    path("users/create/", admin_create_user, name="admin_create_user"),
    path("users/<int:user_id>/view/", admin_view_profile, name="admin_view_profile"),
    path("users/<int:user_id>/edit/", admin_edit_user, name="admin_edit_user"),
    path("users/<int:user_id>/delete/", admin_delete_user, name="admin_delete_user"),
    path("users/<int:user_id>/reset-password/", admin_reset_password, name="admin_reset_password"),
]
