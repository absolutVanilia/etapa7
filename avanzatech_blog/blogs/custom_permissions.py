from rest_framework import permissions
class IsOwnerOrIsAdminPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        print(int(bool(request.user.is_staff)))
        return bool(request.user.is_staff or request.user.is_authenticated)
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.owner == request.user or request.user.is_staff
    
