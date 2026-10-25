from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny

from studioclock.models import Station
from studioclock.serializers import StationSerializer


class StationListCreateAPIView(ListCreateAPIView):
    queryset = Station.objects.all().order_by("name")
    serializer_class = StationSerializer

    def get_permissions(self):
        return [AllowAny()]
