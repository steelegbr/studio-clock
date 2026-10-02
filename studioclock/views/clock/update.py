from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from studioclock.forms.clock import ClockForm
from studioclock.models import Clock


class ClockUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "studioclock.change_clock"
    model = Clock
    template_name = "clock/edit.html"
    form_class = ClockForm
    success_url = reverse_lazy("clock:list")
