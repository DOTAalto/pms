from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied


class OwnerRequiredMixin:
    """
    Checks the ownership of a model object before dispatching a view
    Can only be used in views where a) self.get_object() returns an object and b) there is
    the field owner in the model that points to a user model
    """
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner == request.user or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied


class StaffRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        u = request.user
        if not u.is_authenticated:
            return self.handle_no_permission()
        if not u.is_staff:
            return self.handle_no_permission()
        
        return super().dispatch(request, *args, **kwargs)