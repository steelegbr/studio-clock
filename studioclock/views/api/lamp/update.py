from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from studioclock.models import Lamp
from studioclock.permissions.lamp import CanControlLamps
from studioclock.serializers import LampStateSerializer


class LampUpdateView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, CanControlLamps)

    def put(self, request, slug):
        serializer = LampStateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        lamp = get_object_or_404(Lamp, slug=slug, enabled=True)

        new_state = serializer.validated_data["state"]

        if lamp.state != new_state:
            lamp.state = new_state
            lamp.save(update_fields=["state", "updated"])

        return Response({"slug": lamp.slug, "state": lamp.state})
