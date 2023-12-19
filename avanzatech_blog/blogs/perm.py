from rest_framework.permissions import BasePermission
class IsOwnerOrAdminPermission(BasePermission):
    print("hola")
    def has_permission(self, request, view):
        return bool(request.user.is_staff and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        print('entre en el object')
        return bool(request.user.is_staff or request.user == obj.owner)