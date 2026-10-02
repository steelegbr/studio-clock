from django.views.generic import ListView

from studioclock.models import Clock


class ClockListView(ListView):
    model = Clock
    template_name = "clock/list.html"
    paginate_by = 10
