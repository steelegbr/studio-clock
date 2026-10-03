from django.forms.models import model_to_dict
from django.views.generic import DetailView

from studioclock.models import Clock


class ClockRenderView(DetailView):
    model = Clock
    template_name = "clock/render.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["clock_json"] = model_to_dict(self.object, exclude=["id", "logo"])
        return context
