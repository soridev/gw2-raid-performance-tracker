"""EliteInsider URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import RedirectView
from elite_insider_api import urls as elite_api_urls
from elite_insider_ui import urls as elite_ui_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(url="/elite-ui/login/", permanent=True), name="index"),
    path("api-auth/", include("rest_framework.urls")),
    path("elite-api/", include(elite_api_urls)),
    path("elite-ui/", include(elite_ui_urls)),
]
