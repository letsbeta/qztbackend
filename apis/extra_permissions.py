from rest_framework import permissions

class APPKeyPermission(permissions.BasePermission):
    """
    Global permission check for APP-Key.
    """

    def has_permission(self, request, view):
        if 'HTTP_ACCEPT' in request.META:
            if 'text/html' in request.META['HTTP_ACCEPT']:
                return True
        if not 'HTTP_X_APP_KEY' in request.META:
            return False
        app_key = request.META['HTTP_X_APP_KEY']
        if app_key == "itisreallyhard2guess!":
            return True
        else:
            return False

