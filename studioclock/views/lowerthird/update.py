from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from studioclock.forms.lowerthird import LowerThirdForm
from studioclock.models import LowerThird


class LowerThirdUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "studioclock.change_lowerthird"
    model = LowerThird
    template_name = "lowerthird/edit.html"
    form_class = LowerThirdForm
    success_url = reverse_lazy("lowerthird:list")
