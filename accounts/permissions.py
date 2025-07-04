from rest_framework.permissions import BasePermission, SAFE_METHODS


class ResponsablePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='responsable').exists()
    
    
class ResponsableUpdatePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.groups.filter(name='responsable').exists()
    
    
class IntercesseurPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='intercesseur').exists()
    
    
class IntercesseurUpdatePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.groups.filter(name='intercesseur').exists()
    
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)