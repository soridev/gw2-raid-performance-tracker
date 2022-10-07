from django.urls import path
from .views import main, guilds

urlpatterns = [
    path("dashboard/", main, name="dashboard"),
    path("guilds/", guilds, name="guilds"),
]
