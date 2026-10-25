from rest_framework.serializers import ModelSerializer

from studioclock.models import Song


class SongSerializer(ModelSerializer):
    model = Song
    fields = ("id", "artist", "title", "year")
    read_only_fields = fields
