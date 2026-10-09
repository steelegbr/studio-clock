from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from studioclock.models import Clock
from studioclock.services.now_playing import refresh_now_playing


class NowPlayingStatusView(View):
    def get(self, request, pk):
        clock = get_object_or_404(
            Clock.objects.select_related("now_playing_source"), pk=pk
        )
        source = clock.now_playing_source
        if source is None:
            return JsonResponse(
                {
                    "is_playing": False,
                    "artist": "",
                    "title": "",
                    "artwork_url": "",
                    "poll_interval_seconds": 30,
                }
            )

        refresh_now_playing(source)
        return JsonResponse(
            {
                "is_playing": source.is_playing,
                "artist": source.artist,
                "title": source.title,
                "artwork_url": source.artwork_url,
                "poll_interval_seconds": source.poll_interval_seconds,
            }
        )
