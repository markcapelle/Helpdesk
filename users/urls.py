from django.urls import path
from .views import login_page, register_page, dashboard, logout_page, edit_user

urlpatterns = [
    path("login/", login_page, name="login"),
    path("dashboard/", dashboard, name="dashboard"),
    path("logout/", logout_page, name="logout"),
    path("edit/", edit_user, name="edit_user"),
]
