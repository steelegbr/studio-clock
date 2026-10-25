from rest_framework.serializers import BooleanField, ModelSerializer

from studioclock.models import Song


class NowPlayingSongSerializer(ModelSerializer):
    class Meta:
        model = Song
        fields = ("artist", "title", "year")


class NowPlayingResultSerializer(ModelSerializer):
    is_playing_a_song = BooleanField()
    song = NowPlayingSongSerializer(allow_null=True)
