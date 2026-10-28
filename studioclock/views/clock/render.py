from django.forms.models import model_to_dict
from django.views.generic import DetailView

from studioclock.models import Clock
from studioclock.services.weather import weather_payload


class ClockRenderView(DetailView):
    model = Clock
    template_name = "clock/render.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["clock_json"] = model_to_dict(
            self.object,
            exclude=[
                "id",
                "lamps",
                "logo",
                "weather_latitude",
                "weather_longitude",
                "weather_forecast",
                "weather_last_polled_at",
            ],
        )
        context["weather"] = weather_payload(self.object)
        return context
