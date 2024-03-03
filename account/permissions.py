from rest_framework import permissions
from .models import UserProfile as User

class IsUserOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        # If the request is a read-only request

        if request.method in permissions.SAFE_METHODS:
           
            return True

        if request.user.is_superuser:
            return True

        return obj.id == request.user.id
