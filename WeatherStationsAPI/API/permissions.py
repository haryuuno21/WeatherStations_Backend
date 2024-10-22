from rest_framework import permissions
from API.models import CustomUser
import redis

session_storage = redis.Redis(host='localhost', port=6380, db=0)

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            ssid = request.COOKIES["session_id"]
            username = session_storage.get(ssid)
            user = CustomUser.objects.get(username = username.decode("utf-8"))
        except:
            return False
        return bool(user and (user.is_staff or user.is_superuser))

class IsManagerOrGetOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if(request.method == "GET"):
            return True
        try:
            ssid = request.COOKIES["session_id"]
            username = session_storage.get(ssid)
            user = CustomUser.objects.get(username = username.decode("utf-8"))
        except:
            return False
        return bool(user and (user.is_staff or user.is_superuser))
        
    

class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            ssid = request.COOKIES["session_id"]
            username = session_storage.get(ssid)
            user = CustomUser.objects.get(username = username.decode("utf-8"))
        except:
            return False
        return bool(user)