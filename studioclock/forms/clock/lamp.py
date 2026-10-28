from django.forms import CheckboxSelectMultiple, ModelForm, ModelMultipleChoiceField

from studioclock.models import Clock, Lamp


class ClockLampForm(ModelForm):
    class Meta:
        model = Clock
        fields = ["lamps"]
        widgets = {"lamps": CheckboxSelectMultiple(attrs={"class": "form-check-input"})}

    lamps = ModelMultipleChoiceField(
        queryset=Lamp.objects.filter(enabled=True).order_by("name"),
        required=False,
        widget=CheckboxSelectMultiple,
    )
