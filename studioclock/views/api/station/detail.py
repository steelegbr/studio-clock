from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny

from studioclock.models import Station
from studioclock.serializers import StationSerializer


class StationDetailView(RetrieveAPIView):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    lookup_field = "name"
    lookup_url_kwarg = "name"

    def get_permissions(self):
        return [AllowAny()]
