from rest_framework.routers import DefaultRouter
from .views import CommitteeNoteViewSet, EvaluationViewSet

router = DefaultRouter()
router.register("evaluations", EvaluationViewSet, basename="evaluation")
router.register("committee-notes", CommitteeNoteViewSet, basename="committee-note")
urlpatterns = router.urls
