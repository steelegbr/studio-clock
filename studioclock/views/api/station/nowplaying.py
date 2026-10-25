from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView

from studioclock.models import Station
from studioclock.permissions import CanCreateSongPlay
from studioclock.serializers import (
    NowPlayingResultSerializer,
    SongPlayCreateSerializer,
    SongSerializer,
)


class StationNowPlayingView(APIView):
    authentication_classes = (TokenAuthentication,)

    def get_station(self, name):
        return get_object_or_404(Station, name=name)

    def get(self, request, name):
        station = self.get_station(name)

        latest_play = (
            station.song_plays.select_related("song")
            .order_by("-timestamp", "-pk")
            .first()
        )

        song = latest_play.song if latest_play else None

        result = {
            "is_playing_a_song": song is not None,
            "song": song,
        }

        serializer = NowPlayingResultSerializer(result)
        return Response(serializer.data)

    def post(self, request, name):
        station = self.get_station(name)

        serializer = SongPlayCreateSerializer(
            data=request.data or {},
        )
        serializer.is_valid(raise_exception=True)
        song_play = serializer.save(station=station)

        song = song_play.song

        return Response(
            SongSerializer(song).data if song is not None else None,
            status=HTTP_201_CREATED,
        )

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]

        return [CanCreateSongPlay()]
