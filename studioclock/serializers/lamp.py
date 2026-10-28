from rest_framework.serializers import BooleanField, ModelSerializer, Serializer

from studioclock.models import Lamp


class LampSerializer(ModelSerializer):
    class Meta:
        model = Lamp
        fields = ("slug", "name", "colour", "state")


class LampStateSerializer(Serializer):
    state = BooleanField()
