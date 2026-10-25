from django.urls import include, path

app_name = "clock_api"

urlpatterns = [
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("clock/", include("studioclock.routes.api.clock")),
    path("station/", include("studioclock.routes.api.station")),
]
