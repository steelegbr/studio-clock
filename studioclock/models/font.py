from uuid import uuid4

from django.db.models import (
    CASCADE,
    ForeignKey,
    Model,
    PositiveSmallIntegerField,
    TextChoices,
    TextField,
    UUIDField,
)


class Font(Model):
    class FontCategory(TextChoices):
        SANS_SERIF = "SANS_SERIF", "Sans Serif"
        SERIF = "SERIF", "Serif"
        MONOSPACE = "MONOSPACE", "Monospace"

    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    name = TextField(unique=True, blank=False, null=False)
    family = TextField(unique=True, blank=False, null=False)
    category = TextField(choices=FontCategory.choices, default=FontCategory.SANS_SERIF)

    class Meta:
        ordering = ["name"]
        verbose_name = "Font"
        verbose_name_plural = "Fonts"

    def __str__(self):
        return self.name


class FontWeight(Model):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    font = ForeignKey(Font, on_delete=CASCADE, related_name="weights")
    weight = PositiveSmallIntegerField(blank=False, null=False)
    name = TextField(blank=False, null=False)

    class Meta:
        unique_together = ("font", "weight")
        ordering = ["font", "weight"]
        verbose_name = "Font Weight"
        verbose_name_plural = "Font Weights"

    def __str__(self):
        return f"{self.font.name} ({self.weight}) [{self.font.category}]"
