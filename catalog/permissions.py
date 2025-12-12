from rest_framework.permissions import BasePermission


def is_librarian_user(user) -> bool:
    if not user or not user.is_authenticated:
        return False
    return bool(
        user.is_staff or user.is_superuser or getattr(user, "is_librarian", False)
    )


class IsStaffOrLibrarian(BasePermission):
    """Allow access to Django staff or librarian flagged users."""

    def has_permission(self, request, view):
        return is_librarian_user(request.user)
