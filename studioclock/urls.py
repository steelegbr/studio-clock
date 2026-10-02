"""
URL configuration for studioclock project.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("studioclock.routes.base")),
    path("admin/", admin.site.urls),
]
