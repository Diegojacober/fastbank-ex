from rest_framework import permissions


class IsCreationOrIsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            if view.action == 'create':
                return True
            else:
                return False
        else:
            return True
