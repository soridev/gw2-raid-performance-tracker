from django.urls import path
from .views import main, guilds, login
from .upload_view import upload

urlpatterns = [
    path("login/", login, name="login"),
    path("dashboard/", main, name="dashboard"),
    path("guilds/", guilds, name="guilds"),
    path("upload/", upload, name="ui-upload"),
]
