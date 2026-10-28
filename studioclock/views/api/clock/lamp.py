from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from studioclock.models import Clock
from studioclock.serializers import LampSerializer


class ClockLampView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        clock = get_object_or_404(Clock, pk=pk)
        lamps = clock.lamps.filter(enabled=True).order_by("name")

        serializer = LampSerializer(lamps, many=True)

        return Response({"lamps": serializer.data})
