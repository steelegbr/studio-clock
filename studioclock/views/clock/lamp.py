from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from studioclock.forms.clock import ClockLampForm
from studioclock.models import Clock


class ClockLampView(PermissionRequiredMixin, UpdateView):
    permission_required = "studioclock.change_clock"
    model = Clock
    template_name = "clock/lamp.html"
    form_class = ClockLampForm
    success_url = reverse_lazy("clock:list")
