from uuid import uuid4

from django.db.models import Model, PositiveIntegerField, TextField, URLField, UUIDField

from studioclock.validators import valid_year


class Song(Model):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    artist = TextField(blank=False, null=False)
    title = TextField(blank=False, null=False)
    year = PositiveIntegerField(
        null=True,
        validators=[valid_year],
    )
    artwork_url = URLField(null=True)

    def __str__(self):
        if self.year:
            return f"{self.artist} - {self.title} ({self.year})"
        return f"{self.artist} - {self.title}"

    class Meta:
        ordering = ["artist", "title"]
        unique_together = ("artist", "title")
        verbose_name = "Song"
        verbose_name_plural = "Songs"
