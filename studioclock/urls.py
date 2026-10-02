"""
URL configuration for studioclock project.
"""

from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import include, path

from studioclock.forms.auth import LoginForm

urlpatterns = [
    path("", include("studioclock.routes.base")),
    path("admin/", admin.site.urls),
    path("clock/", include("studioclock.routes.clock")),
    path(
        "users/login/", LoginView.as_view(authentication_form=LoginForm), name="login"
    ),
    path("users/", include("django.contrib.auth.urls")),
]
