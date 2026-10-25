from django.urls import path

from studioclock.views.lowerthird import LowerThirdListView

app_name = "lowerthird"

urlpatterns = [
    path("", LowerThirdListView.as_view(), name="list"),
]
