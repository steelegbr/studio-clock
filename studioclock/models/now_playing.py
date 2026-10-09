from uuid import uuid4

from django.core.validators import MinValueValidator
from django.db.models import (
    BooleanField,
    CharField,
    DateTimeField,
    Model,
    PositiveSmallIntegerField,
    URLField,
    UUIDField,
)


class NowPlayingSource(Model):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    name = CharField(max_length=100, unique=True)
    endpoint_url = URLField()
    poll_interval_seconds = PositiveSmallIntegerField(
        default=30, validators=[MinValueValidator(5)]
    )
    enabled = BooleanField(default=True)
    artist = CharField(max_length=255, blank=True)
    title = CharField(max_length=255, blank=True)
    artwork_url = URLField(blank=True)
    is_playing = BooleanField(default=False)
    last_polled_at = DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Now Playing Source"
        verbose_name_plural = "Now Playing Sources"

    def __str__(self):
        return self.name
