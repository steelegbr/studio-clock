from uuid import uuid4

from colorfield.fields import ColorField
from django.db.models import (
    CASCADE,
    SET_NULL,
    ForeignKey,
    ImageField,
    Model,
    TextChoices,
    TextField,
    UUIDField,
)


class Clock(Model):
    class ClockType(TextChoices):
        LED = "LED", "LED"
        SWEEPING = "SWEEPING", "Sweeping"

    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    name = TextField(unique=True, blank=False, null=False)
    description = TextField(blank=True, null=True)
    clock_type = TextField(choices=ClockType.choices, default=ClockType.LED)
    led_colour = ColorField(default="#FF0000", blank=False, null=False)
    led_background_colour = ColorField(default="#000000", blank=False, null=False)
    sweeping_background_colour = ColorField(default="#FFFFFF", blank=False, null=False)
    sweeping_hour_hand_colour = ColorField(default="#000000", blank=False, null=False)
    sweeping_minute_hand_colour = ColorField(default="#000000", blank=False, null=False)
    sweeping_second_hand_colour = ColorField(default="#FF0000", blank=False, null=False)
    sweeping_stroke_colour = ColorField(default="#000000", blank=False, null=False)
    logo = ImageField(upload_to="logos/", blank=True, null=True)
    background_colour = ColorField(default="#FFFFFF", blank=False, null=False)
    foreground_colour = ColorField(default="#000000", blank=False, null=False)
    font = ForeignKey("FontWeight", on_delete=CASCADE, blank=True, null=True)
    now_playing_source = ForeignKey(
        "NowPlayingSource",
        on_delete=SET_NULL,
        blank=True,
        null=True,
        related_name="clocks",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Clock"
        verbose_name_plural = "Clocks"
