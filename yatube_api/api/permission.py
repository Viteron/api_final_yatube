"""Модуль с разрешениями."""
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user

    def has_object_permission(self, request, view, obj):
        return (request.method
                in permissions.SAFE_METHODS
                or obj.author == request.user)
