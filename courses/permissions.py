from rest_framework.permissions import BasePermission


class isInstructor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'instructor'
