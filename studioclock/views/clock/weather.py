from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from studioclock.models import Clock
from studioclock.services.weather import weather_payload


class WeatherStatusView(View):
    def get(self, request, pk):
        clock = get_object_or_404(Clock, pk=pk)
        return JsonResponse(weather_payload(clock))
