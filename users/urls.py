from django.urls import path
from .views import login_page, register_page, dashboard, logout_page

urlpatterns = [
    path("login/", login_page, name="login"),
    path("register/", register_page, name="register"),
    path("dashboard/", dashboard, name="dashboard"),
    path("logout/", logout_page, name="logout"),
]
