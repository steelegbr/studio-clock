from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from studioclock.models import Clock


class NowPlayingStatusView(APIView):
    def get(self, request, pk):
        clock = get_object_or_404(Clock.objects.select_related("station"), pk=pk)
        station = clock.station

        if station is None:
            return Response(self.empty_status())

        song_play = station.song_plays.order_by(
            "-timestamp",
            "-pk",
        ).first()

        if not song_play.song:
            return Response(self.empty_status())

        return Response(
            {
                "is_playing": True,
                "artist": song_play.song.artist,
                "title": song_play.song.title,
                "artwork_url": song_play.song.artwork_url or "",
                "poll_interval_seconds": 30,
            }
        )

    @staticmethod
    def empty_status():
        return {
            "is_playing": False,
            "artist": "",
            "title": "",
            "artwork_url": "",
            "poll_interval_seconds": 30,
        }
