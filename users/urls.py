from django.urls import path
from .views import login_page, dashboard, logout_page, edit_user, user_reset_password, view_profile

urlpatterns = [
    path("login/", login_page, name="login"),
    path("dashboard/", dashboard, name="dashboard"),
    path("logout/", logout_page, name="logout"),
    path("edit/", edit_user, name="edit_user"),
    path("reset-password/", user_reset_password, name="user_reset_password"),
    path("profile/", view_profile, name="view_profile"),
]
