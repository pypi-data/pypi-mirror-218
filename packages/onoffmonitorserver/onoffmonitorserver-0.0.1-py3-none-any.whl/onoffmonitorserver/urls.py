from rest_framework.routers import DefaultRouter

from .views import DeviceViewSet, StatusViewSet

router = DefaultRouter()
router.register('device', DeviceViewSet)
router.register('status', StatusViewSet)

urlpatterns = router.urls
