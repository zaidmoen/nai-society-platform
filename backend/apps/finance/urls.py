from rest_framework.routers import DefaultRouter
from .views import FinanceTransactionViewSet

router = DefaultRouter()
router.register("finance/transactions", FinanceTransactionViewSet, basename="finance-transaction")
urlpatterns = router.urls
