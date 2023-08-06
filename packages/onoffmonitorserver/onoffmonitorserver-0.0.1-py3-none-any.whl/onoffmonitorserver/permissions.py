from rest_framework.permissions import BasePermission


class IsDeviceOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsStatusOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.device.user == request.user
