from django.urls import path

from studioclock.views.api.station import (
    StationDetailView,
    StationListCreateAPIView,
    StationNowPlayingView,
)

urlpatterns = [
    path("", StationListCreateAPIView.as_view(), name="station-list"),
    path("<str:name>/", StationDetailView.as_view(), name="station-detail"),
    path(
        "<str:name>/now-playing/",
        StationNowPlayingView.as_view(),
        name="station-now-playing",
    ),
]
