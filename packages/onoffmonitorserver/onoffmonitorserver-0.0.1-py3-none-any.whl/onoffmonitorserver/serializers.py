from rest_framework.serializers import ModelSerializer, ValidationError, CurrentUserDefault, HiddenField

from . import models


class DeviceSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    class Meta:
        model = models.Device
        fields = ['id', 'name', 'user']


class StatusSerializer(ModelSerializer):
    def validate(self, attrs):
        if attrs['device'].user != CurrentUserDefault()(self):
            raise ValidationError('Device owner must be the current user')
        return super().validate(attrs)

    class Meta:
        model = models.Status
        fields = ['id', 'device', 'status', 'time']
