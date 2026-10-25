from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from studioclock.forms.lowerthird import LowerThirdForm
from studioclock.models import LowerThird


class LowerThirdCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "studioclock.add_lowerthird"
    model = LowerThird
    form_class = LowerThirdForm
    template_name = "lowerthird/create.html"
    success_url = reverse_lazy("lowerthird:list")
