from django.urls import path

from studioclock.views.api.clock import ClockNowPlayingView, ClockWeatherView

urlpatterns = [
    path("<uuid:pk>/now-playing/", ClockNowPlayingView.as_view(), name="now-playing"),
    path("<uuid:pk>/weather/", ClockWeatherView.as_view(), name="weather"),
]
