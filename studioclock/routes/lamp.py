from django.urls import path

from studioclock.views.lamp import (
    LampCreateView,
    LampDeleteView,
    LampListView,
    LampUpdateView,
)

app_name = "lamp"

urlpatterns = [
    path("create/", LampCreateView.as_view(), name="create"),
    path("<uuid:pk>/edit/", LampUpdateView.as_view(), name="edit"),
    path("<uuid:pk>/delete/", LampDeleteView.as_view(), name="delete"),
    path("", LampListView.as_view(), name="list"),
]
