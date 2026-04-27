from rest_framework.permissions import BasePermission



class isProfileUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return self.request.user.id == obj.user.id