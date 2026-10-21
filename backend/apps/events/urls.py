from rest_framework.routers import DefaultRouter
from .views import AvailabilityViewSet, EventViewSet

router = DefaultRouter()
router.register("events", EventViewSet, basename="event")
router.register("availability", AvailabilityViewSet, basename="availability")
urlpatterns = router.urls
