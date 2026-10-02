from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from studioclock.models import Clock


class ClockDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "studioclock.delete_clock"
    model = Clock
    template_name = "clock/delete.html"
    success_url = reverse_lazy("clock:list")
