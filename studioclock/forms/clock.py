from django.forms import ModelForm, Select, Textarea, TextInput

from studioclock.models import Clock


class ClockForm(ModelForm):
    class Meta:
        model = Clock
        fields = ["name", "description", "clock_type"]
        widgets = {
            "name": TextInput(attrs={"class": "form-control"}),
            "description": Textarea(attrs={"class": "form-control"}),
            "clock_type": Select(attrs={"class": "form-select"}),
        }
