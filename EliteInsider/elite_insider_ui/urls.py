from django.urls import path
from .views import main, guilds, user_login
from .upload_view import upload

urlpatterns = [
    path("login/", user_login, name="user-login"),
    path("dashboard/", main, name="dashboard"),
    path("guilds/", guilds, name="guilds"),
    path("upload/", upload, name="ui-upload"),
]
