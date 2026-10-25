from uuid import uuid4

from django.db.models import CASCADE, DateTimeField, ForeignKey, Model, UUIDField


class SongPlay(Model):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    song = ForeignKey("Song", null=True, on_delete=CASCADE)
    station = ForeignKey(
        "Station", null=False, related_name="song_plays", on_delete=CASCADE
    )
    timestamp = DateTimeField(auto_created=True)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Song Play"
        verbose_name_plural = "Song Plays"
