from rest_framework.serializers import ModelSerializer

from studioclock.models import Station


class StationSerializer(ModelSerializer):
    class Meta:
        model = Station
        fields = ("id", "name")
        read_only_fields = ("id",)
