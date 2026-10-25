from django.urls import path

from studioclock.views.lowerthird import (
    LowerThirdCreateView,
    LowerThirdDeleteView,
    LowerThirdListView,
    LowerThirdRenderView,
    LowerThirdUpdateView,
)

app_name = "lowerthird"

urlpatterns = [
    path("create/", LowerThirdCreateView.as_view(), name="create"),
    path("<uuid:pk>/", LowerThirdRenderView.as_view(), name="render"),
    path("<uuid:pk>/edit/", LowerThirdUpdateView.as_view(), name="edit"),
    path("<uuid:pk>/delete/", LowerThirdDeleteView.as_view(), name="delete"),
    path("", LowerThirdListView.as_view(), name="list"),
]
