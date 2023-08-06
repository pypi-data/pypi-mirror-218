from rest_framework.filters import BaseFilterBackend


class DeviceOwnerFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(user=request.user)


class StatusOwnerFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(device__user=request.user)
