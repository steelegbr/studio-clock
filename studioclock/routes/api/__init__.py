from django.urls import include, path

app_name = "clock_api"

urlpatterns = [
    path("clock/", include("studioclock.routes.api.clock")),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
