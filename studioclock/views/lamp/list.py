from django.views.generic import ListView

from studioclock.models import Lamp


class LampListView(ListView):
    model = Lamp
    template_name = "lamp/list.html"
    paginate_by = 10
