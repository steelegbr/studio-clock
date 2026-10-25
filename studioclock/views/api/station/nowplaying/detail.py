from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from studioclock.models import Station
from studioclock.serializers import NowPlayingResultSerializer


class SongPlayDetailView(APIView):
    def get(self, request, name):
        station = get_object_or_404(
            Station.objects.prefetch_related("song_plays__song"),
            name=name,
        )

        latest_play = station.song_plays.order_by(
            "-timestamp",
            "-pk",
        ).first()

        song = latest_play.song if latest_play else None

        result = {
            "is_playing_a_song": song is not None,
            "song": song,
        }

        serializer = NowPlayingResultSerializer(result)
        return Response(serializer.data)
