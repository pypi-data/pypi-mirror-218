# pylint:disable=no-member
from knox.auth import TokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from . import models
from .filters import DeviceOwnerFilter, StatusOwnerFilter
from .permissions import IsDeviceOwner, IsStatusOwner
from .serializers import DeviceSerializer, StatusSerializer


class DeviceViewSet(ModelViewSet):
    queryset = models.Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated, IsDeviceOwner]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    filter_backends = [DeviceOwnerFilter]


class StatusViewSet(ModelViewSet):
    queryset = models.Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAuthenticated, IsStatusOwner]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    filter_backends = [StatusOwnerFilter]
