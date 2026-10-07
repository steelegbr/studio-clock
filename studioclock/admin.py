from django.contrib.admin import register
from unfold.admin import ModelAdmin

from studioclock.models import Clock, Font, FontWeight


@register(Clock)
class ClockAdmin(ModelAdmin):
    list_display = ("name", "clock_type", "led_colour")
    search_fields = ("name",)


@register(Font)
class FontAdmin(ModelAdmin):
    list_display = ("name", "family", "category")
    search_fields = ("name", "family")


@register(FontWeight)
class FontWeightAdmin(ModelAdmin):
    list_display = ("font", "weight", "name")
    search_fields = ("font__name", "name")
