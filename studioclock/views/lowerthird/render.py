from django.views.generic import DetailView

from studioclock.models import LowerThird


class LowerThirdRenderView(DetailView):
    model = LowerThird
    template_name = "lowerthird/render.html"
