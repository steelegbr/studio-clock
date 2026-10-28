from django.urls import path

from studioclock.views.api.clock import (
    ClockLampView,
    ClockNowPlayingView,
    ClockWeatherView,
)

urlpatterns = [
    path("<uuid:pk>/lamps/", ClockLampView.as_view(), name="lamps"),
    path("<uuid:pk>/now-playing/", ClockNowPlayingView.as_view(), name="now-playing"),
    path("<uuid:pk>/weather/", ClockWeatherView.as_view(), name="weather"),
]
