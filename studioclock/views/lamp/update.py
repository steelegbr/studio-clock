from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from studioclock.forms.lamp import LampForm
from studioclock.models import Lamp


class LampUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "studioclock.change_lamp"
    model = Lamp
    template_name = "lamp/edit.html"
    form_class = LampForm
    success_url = reverse_lazy("lamp:list")
