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
        ]
        labels = {
            "led_colour": "LED colour",
            "led_background_colour": "LED background colour",
        }
        widgets = {
            "name": TextInput(attrs={"class": "form-control"}),
            "description": Textarea(attrs={"class": "form-control"}),
            "clock_type": Select(attrs={"class": "form-select"}),
            "led_colour": ColorWidget(),
            "led_background_colour": ColorWidget(),
        }
