from rest_framework import filters


def is_superadmin(user) -> bool:
    return user.is_superuser or user.groups.filter(name='admin').exists()


class ActiveRecordsFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        is_active = request.query_params.get('isActive', None)
        is_admin = is_superadmin(user)

        if not is_admin or is_active == "true":
            queryset = queryset.filter(is_active=True)
        if is_admin and is_active == "false":
            queryset = queryset.filter(is_active=False)
        return queryset
