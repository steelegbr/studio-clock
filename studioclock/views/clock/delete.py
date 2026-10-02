from django.urls import reverse_lazy
from django.views.generic import DeleteView

from studioclock.models import Clock


class ClockDeleteView(DeleteView):
    model = Clock
    template_name = "clock/delete.html"
    success_url = reverse_lazy("clock:list")
