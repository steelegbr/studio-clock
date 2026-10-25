from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from studioclock.models import Clock
from studioclock.services.weather import weather_payload


class ClockWeatherView(APIView):
    def get(self, request, pk):
        clock = get_object_or_404(Clock, pk=pk)
        return Response(weather_payload(clock))

    def get_permissions(self):
        return [AllowAny()]
