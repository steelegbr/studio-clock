from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from studioclock.models import Station
from studioclock.serializers import SongPlayCreateSerializer, SongSerializer


class SongPlayCreateView(CreateAPIView):
    serializer_class = SongPlayCreateSerializer

    def get_station(self):
        return get_object_or_404(Station, name=self.kwargs["name"])

    def create(self, request, *args, **kwargs):
        data = request.data
        if data is None:
            data = {}

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        song_play = serializer.save(station=self.get_station())

        return Response(
            SongSerializer(song_play.song).data if song_play.song is not None else None,
            status=HTTP_201_CREATED,
        )
