from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class OwnerRequiredMixin:
    """
    Checks the ownership of a model object before dispatching a view
    Can only be used in views where a) self.get_object() returns an object and b) there is
    the field owner in the model that points to a user model
    """
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        print(obj.owner)
        print(request.user)
        if obj.owner != request.user or not request.user.is_superuser:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)