from django.urls import reverse_lazy
from django.views.generic import CreateView

from studioclock.forms.clock import ClockForm
from studioclock.models import Clock


class ClockCreateView(CreateView):
    model = Clock
    form_class = ClockForm
    template_name = "clock/create.html"
    success_url = reverse_lazy("clock:list")
