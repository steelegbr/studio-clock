from django.contrib.admin import register
from unfold.admin import ModelAdmin

from studioclock.models import Clock


@register(Clock)
class ClockAdmin(ModelAdmin):
    list_display = ("name", "clock_type", "led_colour")
    search_fields = ("name",)
