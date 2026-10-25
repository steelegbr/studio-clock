from rest_framework.generics import ListCreateAPIView

from studioclock.models import Station
from studioclock.serializers import StationSerializer


class StationListCreateAPIView(ListCreateAPIView):
    queryset = Station.objects.all().order_by("name")
    serializer_class = StationSerializer
