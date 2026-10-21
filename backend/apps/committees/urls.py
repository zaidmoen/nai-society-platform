from rest_framework.routers import DefaultRouter
from .views import CommitteeViewSet

router = DefaultRouter()
router.register("committees", CommitteeViewSet, basename="committee")
urlpatterns = router.urls
