import functools

from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response


def check_retrieve():
    def decorator(drf_custom_method):
        @functools.wraps(drf_custom_method)
        def _decorator(self, request, pk, *args, **kwargs):
            model = self.serializer_class().Meta.model
            obj = self.get_object()
            if getattr(model, "user_can_retrieve_me", None):
                user_can_retrieve = model().user_can_retrieve_me(obj, request.user)
                if not user_can_retrieve:
                    return Response({"error": _("User not authorized to retrieve")},
                                    status=status.HTTP_400_BAD_REQUEST)

            return drf_custom_method(self, request, pk, *args, **kwargs)
        return _decorator

    return decorator
