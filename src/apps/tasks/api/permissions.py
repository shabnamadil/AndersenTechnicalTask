from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthenticatedReadOnlyOrAuthor(BasePermission):
    """
    Allow read-only access for any authenticated user.
    Allow write access only to the author of the task.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return obj.user == request.user
