from rest_framework.generics import RetrieveAPIView

from studioclock.models import Station
from studioclock.serializers import StationSerializer


class StationDetailView(RetrieveAPIView):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    lookup_field = "name"
    lookup_url_kwarg = "name"
