from django.urls import path

from studioclock.views.clock import (
    ClockCreateView,
    ClockDeleteView,
    ClockLampView,
    ClockListView,
    ClockRenderView,
    ClockUpdateView,
)

app_name = "clock"

urlpatterns = [
    path("create/", ClockCreateView.as_view(), name="create"),
    path("<uuid:pk>/", ClockRenderView.as_view(), name="render"),
    path("<uuid:pk>/edit/", ClockUpdateView.as_view(), name="edit"),
    path("<uuid:pk>/delete/", ClockDeleteView.as_view(), name="delete"),
    path("<uuid:pk>/lamps/", ClockLampView.as_view(), name="lamps"),
    path("", ClockListView.as_view(), name="list"),
]
