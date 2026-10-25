from uuid import uuid4

from colorfield.fields import ColorField
from django.db.models import CASCADE, ForeignKey, Model, TextField, UUIDField


class LowerThird(Model):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    name = TextField(unique=True, blank=False, null=False)
    description = TextField(blank=True, null=True)
    background_colour = ColorField(default="#FFFFFF", blank=False, null=False)
    foreground_colour = ColorField(default="#000000", blank=False, null=False)
    station = ForeignKey("Station", null=False, on_delete=CASCADE)
    font = ForeignKey("FontWeight", on_delete=CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Lower Third"
        verbose_name_plural = "Lower Thirds"
