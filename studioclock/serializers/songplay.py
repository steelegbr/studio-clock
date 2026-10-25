from rest_framework.serializers import (
    CharField,
    IntegerField,
    ModelSerializer,
    ValidationError,
)

from studioclock.models import Song, SongPlay


class SongPlayCreateSerializer(ModelSerializer):
    artist = CharField(required=False)
    title = CharField(required=False)
    year = IntegerField(required=False, allow_null=True, min_value=1000, max_value=9999)

    def validate(self, attrs):
        has_artist = "artist" in attrs
        has_title = "title" in attrs

        if has_artist != has_title:
            raise ValidationError(
                "We must have either both artist and title, or neither"
            )

        if "year" in attrs and not has_artist:
            raise ValidationError("You cannot send a year without an artist and title")

        return attrs

    def create(self, validated_data):
        station = validated_data.pop("station")
        artist = validated_data.pop("artist", None)
        title = validated_data.pop("title", None)
        year = validated_data.pop("year", None)

        song = None

        if artist is not None:
            song, _ = Song.objects.get_or_create(
                artist=artist,
                title=title,
                year=year,
            )

        return SongPlay.objects.create(
            station=station,
            song=song,
        )
