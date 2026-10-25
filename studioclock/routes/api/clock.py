from django.urls import path

from studioclock.views.api.clock import NowPlayingStatusView

urlpatterns = [
    path("<uuid:pk>/now-playing/", NowPlayingStatusView.as_view(), name="now-playing")
]
