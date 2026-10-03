from colorfield.widgets import ColorWidget
from django.forms import ModelForm, Select, Textarea, TextInput

from studioclock.models import Clock


class ClockForm(ModelForm):
    class Meta:
        model = Clock
        fields = [
            "name",
            "description",
            "clock_type",
            "led_colour",
            "led_background_colour",
            "sweeping_background_colour",
            "sweeping_hour_hand_colour",
            "sweeping_minute_hand_colour",
            "sweeping_second_hand_colour",
        ]
        labels = {
            "led_colour": "LED colour",
            "led_background_colour": "LED background colour",
            "sweeping_background_colour": "Sweeping background colour",
            "sweeping_hour_hand_colour": "Sweeping hour hand colour",
            "sweeping_minute_hand_colour": "Sweeping minute hand colour",
            "sweeping_second_hand_colour": "Sweeping second hand colour",
            "sweeping_stroke_colour": "Sweeping stroke colour",
        }
        widgets = {
            "name": TextInput(attrs={"class": "form-control"}),
            "description": Textarea(attrs={"class": "form-control"}),
            "clock_type": Select(attrs={"class": "form-select"}),
            "led_colour": ColorWidget(),
            "led_background_colour": ColorWidget(),
            "sweeping_background_colour": ColorWidget(),
            "sweeping_hour_hand_colour": ColorWidget(),
            "sweeping_minute_hand_colour": ColorWidget(),
            "sweeping_second_hand_colour": ColorWidget(),
            "sweeping_stroke_colour": ColorWidget(),
        }
