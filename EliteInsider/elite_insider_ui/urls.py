from django.urls import path
from .views import main, guilds, login_view, logout_view
from .upload_view import upload

urlpatterns = [
    path("login/", login_view, name="user-login"),
    path("logout/", logout_view, name="logout"),
    path("dashboard/", main, name="dashboard"),
    path("guilds/", guilds, name="guilds"),
    path("upload/", upload, name="ui-upload"),
]
