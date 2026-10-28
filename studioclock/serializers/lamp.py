from rest_framework.serializers import BooleanField, Serializer


class LampStateSerializer(Serializer):
    state = BooleanField()
