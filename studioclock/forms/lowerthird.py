from colorfield.widgets import ColorWidget
from django.forms import ModelForm, Select, Textarea, TextInput

from studioclock.models import LowerThird


class LowerThirdForm(ModelForm):
    class Meta:
        model = LowerThird
        fields = [
            "name",
            "description",
            "station",
            "background_colour",
            "foreground_colour",
            "font",
        ]
        widgets = {
            "name": TextInput(attrs={"class": "form-control"}),
            "description": Textarea(attrs={"class": "form-control"}),
            "station": Select(attrs={"class": "form-select"}),
            "background_colour": ColorWidget(),
            "foreground_colour": ColorWidget(),
            "font": Select(attrs={"class": "form-select"}),
        }
