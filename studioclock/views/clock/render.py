from django.forms.models import model_to_dict
from django.views.generic import DetailView

from studioclock.models import Clock
from studioclock.services.now_playing import refresh_now_playing
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
                "logo",
                "weather_latitude",
                "weather_longitude",
                "weather_forecast",
                "weather_last_polled_at",
            ],
        )
        source = self.object.now_playing_source
        context["now_playing"] = refresh_now_playing(source) if source else None
        context["weather"] = weather_payload(self.object)
        return context
