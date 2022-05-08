from rest_framework import permissions


class IsProfileOwnerOrReadOnly(permissions.BasePermission):
    """
    Is profile owner?
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id


class IsPostAuthorOrReadOnly(permissions.BasePermission):
    """
    Is post author?
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.post_author == request.user


class IsCommentAuthorOrReadOnly(permissions.BasePermission):
    """
    Is comment author?
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.comment_author == request.user
