from uuid import uuid4

from django.db.models import Model, TextField, UUIDField


class Station(Model):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    name = TextField(unique=True, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Radio Station"
        verbose_name_plural = "Radio Stations"
