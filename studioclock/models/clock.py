from uuid import uuid4

from django.db.models import Model, TextChoices, TextField, UUIDField


class Clock(Model):
    class ClockType(TextChoices):
        LED = "LED", "LED"
        SWEEPING = "SWEEPING", "Sweeping"

    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    name = TextField(unique=True, blank=False, null=False)
    description = TextField(blank=True, null=True)
    clock_type = TextField(choices=ClockType.choices, default=ClockType.LED)

    class Meta:
        verbose_name = "Clock"
        verbose_name_plural = "Clocks"
