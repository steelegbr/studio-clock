from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from studioclock.models import LowerThird


class LowerThirdDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "studioclock.delete_lowerthid"
    model = LowerThird
    template_name = "lowerthird/delete.html"
    success_url = reverse_lazy("lowerthird:list")
