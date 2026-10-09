from uuid import uuid4

from colorfield.fields import ColorField
from django.db.models import (
    CASCADE,
    SET_NULL,
    DateTimeField,
    FloatField,
    ForeignKey,
    ImageField,
    JSONField,
    Model,
    TextChoices,
    TextField,
    UUIDField,
)


class Clock(Model):
    class ClockType(TextChoices):
        LED = "LED", "LED"
        SWEEPING = "SWEEPING", "Sweeping"

    class WeatherUnits(TextChoices):
        CELSIUS = "celsius", "Celsius (°C)"
        FAHRENHEIT = "fahrenheit", "Fahrenheit (°F)"

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
    weather_location = TextField(blank=True)
    weather_units = TextField(
        choices=WeatherUnits.choices, default=WeatherUnits.CELSIUS
    )
    weather_latitude = FloatField(blank=True, null=True)
    weather_longitude = FloatField(blank=True, null=True)
    weather_forecast = JSONField(blank=True, default=list)
    weather_last_polled_at = DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        update_fields = kwargs.get("update_fields")
        changed_settings = {"weather_location", "weather_units"}
        if update_fields is not None:
            changed_settings &= set(update_fields)

        if not self._state.adding and self.pk and changed_settings:
            stored_settings = (
                type(self).objects.filter(pk=self.pk).values(*changed_settings).first()
            )
            if stored_settings and any(
                getattr(self, field) != value
                for field, value in stored_settings.items()
            ):
                self.weather_latitude = None
                self.weather_longitude = None
                self.weather_forecast = []
                self.weather_last_polled_at = None
                if update_fields is not None:
                    kwargs["update_fields"] = set(update_fields) | {
                        "weather_latitude",
                        "weather_longitude",
                        "weather_forecast",
                        "weather_last_polled_at",
                    }

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["name"]
        verbose_name = "Clock"
        verbose_name_plural = "Clocks"
