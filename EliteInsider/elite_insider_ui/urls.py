from django.urls import path
from .views import main, guilds
from .upload_view import upload

urlpatterns = [
    path("dashboard/", main, name="dashboard"),
    path("guilds/", guilds, name="guilds"),
    path("upload/", upload, name="ui-upload"),
]
