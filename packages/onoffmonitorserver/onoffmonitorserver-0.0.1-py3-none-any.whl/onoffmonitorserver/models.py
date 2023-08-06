"""
Model classes to represent database tables
"""
from django.conf import settings
from django.db import models
from django.utils import timezone


class Device(models.Model):
    """
    Model for storing data about a device (such as "boiler")
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


class Status(models.Model):
    """
    Model for storing the status of a device (on or off) at a given time
    """
    STATUS_CHOICES = (
        (0, 'Off'),
        (1, 'On'),
    )
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES, default=0)
    time = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'Statuses'
