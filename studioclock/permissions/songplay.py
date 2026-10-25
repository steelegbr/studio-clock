from rest_framework.permissions import BasePermission


class CanCreateSongPlay(BasePermission):
    message = "You do not have permission to create song plays."

    def has_permission(self, request, view):
        return request.user.has_perm("studioclock.add_songplay")
