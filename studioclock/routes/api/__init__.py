from django.urls import include, path

from studioclock.views.api.status import StatusView

app_name = "clock_api"

urlpatterns = [
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("clock/", include("studioclock.routes.api.clock")),
    path("lamp/", include("studioclock.routes.api.lamp")),
    path("station/", include("studioclock.routes.api.station")),
    path("status/", StatusView.as_view()),
]
