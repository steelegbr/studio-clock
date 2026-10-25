from django.views.generic import ListView

from studioclock.models import LowerThird


class LowerThirdListView(ListView):
    model = LowerThird
    template_name = "lowerthird/list.html"
    paginate_by = 10
