from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from studioclock.models import Lamp


class LampDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "studioclock.delete_lamp"
    model = Lamp
    template_name = "lamp/delete.html"
    success_url = reverse_lazy("lamp:list")
