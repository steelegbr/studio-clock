from uuid import uuid4

from django.db.models import (
    BooleanField,
    DateTimeField,
    Model,
    SlugField,
    TextField,
    UUIDField,
)


class Lamp(Model):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    slug = SlugField(unique=True, help_text="Stable API identifier, e.g. mic-live")
    name = TextField(unique=True)
    enabled = BooleanField(default=True)
    state = BooleanField(default=False)
    updated = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Lamp"
        verbose_name_plural = "Lamps"
