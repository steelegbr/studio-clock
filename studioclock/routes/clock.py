from django.urls import path

from studioclock.views.clock import (
    ClockCreateView,
    ClockDeleteView,
    ClockListView,
    ClockRenderView,
    ClockUpdateView,
    NowPlayingStatusView,
)

app_name = "clock"

urlpatterns = [
    path("create/", ClockCreateView.as_view(), name="create"),
    path(
        "<uuid:pk>/now-playing/",
        NowPlayingStatusView.as_view(),
        name="now-playing",
    ),
    path("<uuid:pk>/", ClockRenderView.as_view(), name="render"),
    path("<uuid:pk>/edit/", ClockUpdateView.as_view(), name="edit"),
    path("<uuid:pk>/delete/", ClockDeleteView.as_view(), name="delete"),
    path("", ClockListView.as_view(), name="list"),
]
