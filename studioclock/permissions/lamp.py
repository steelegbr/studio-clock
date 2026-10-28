from rest_framework.permissions import BasePermission

from studioclock.models import Lamp


class CanControlLamps(BasePermission):
    def has_permission(self, request, view):
        permission = f"{Lamp._meta.app_label}.change_lamp"
        return request.user.has_perm(permission)
