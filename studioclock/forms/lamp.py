from django.forms import CheckboxInput, ModelForm, TextInput

from studioclock.models import Lamp


class LampForm(ModelForm):
    class Meta:
        model = Lamp
        fields = ["name", "slug", "enabled"]
        widgets = {
            "name": TextInput(attrs={"class": "form-control"}),
            "slug": TextInput(attrs={"class": "form-control"}),
            "enabled": CheckboxInput(attrs={"class": "form-control"}),
        }
