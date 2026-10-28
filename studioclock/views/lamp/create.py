from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from studioclock.forms.lamp import LampForm
from studioclock.models import Lamp


class LampCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "studioclock.add_lamp"
    model = Lamp
    form_class = LampForm
    template_name = "lamp/create.html"
    success_url = reverse_lazy("lamp:list")
