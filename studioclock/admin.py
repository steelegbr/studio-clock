from django.contrib.admin import register
from unfold.admin import ModelAdmin

from studioclock.models import (
    Clock,
    Font,
    FontWeight,
    Lamp,
    LowerThird,
    Song,
    SongPlay,
    Station,
)


@register(Clock)
class ClockAdmin(ModelAdmin):
    list_display = ("name", "clock_type")
    search_fields = ("name",)


@register(Font)
class FontAdmin(ModelAdmin):
    list_display = ("name", "family", "category")
    search_fields = ("name", "family")


@register(FontWeight)
class FontWeightAdmin(ModelAdmin):
    list_display = ("font", "weight", "name")
    search_fields = ("font__name", "name")


@register(Lamp)
class LampAdmin(ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")


@register(LowerThird)
class LowerThirdAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@register(Song)
class SongAdmin(ModelAdmin):
    list_display = ("artist", "title", "year")
    search_fields = ("artist", "title", "year")


@register(SongPlay)
class SongPlayAdmin(ModelAdmin):
    list_display = ("timestamp", "station", "song")
    search_fields = ("timestamp", "station", "song")


@register(Station)
class StationAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
