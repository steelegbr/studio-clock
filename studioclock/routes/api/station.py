from django.urls import path

from studioclock.views.api.station import (
    SongPlayCreateView,
    SongPlayDetailView,
    StationDetailView,
    StationListCreateAPIView,
)

urlpatterns = [
    path("", StationListCreateAPIView.as_view(), name="station-list"),
    path("<str:name>/", StationDetailView.as_view(), name="station-detail"),
    path(
        "<str:name>/now-playing/",
        SongPlayCreateView.as_view(),
        name="station-songplay-create",
    ),
    path(
        "<str:name>/now-playing/",
        SongPlayDetailView.as_view(),
        name="station-songplay-detail",
    ),
]
