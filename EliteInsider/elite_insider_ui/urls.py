from django.urls import path
from .views import *
from .upload_view import upload

urlpatterns = [
    path("login/", login_view, name="user-login"),
    path("logout/", logout_view, name="logout"),
    path("", main, name="home"),
    path("dashboard/", dashboard, name="dashboard"),
    path("guilds/", guilds, name="guilds"),
    path("upload/", upload, name="ui-upload"),
]
