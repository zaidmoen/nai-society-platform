from django.db import transaction
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from apps.core.access import has_any_role
from apps.core.models import UserRoleAssignment
from .models import FinanceTransaction
from .serializers import FinanceDecisionSerializer, FinanceTransactionSerializer

class FinanceTransactionViewSet(viewsets.ModelViewSet):
    serializer_class = FinanceTransactionSerializer

    def has_permission_for(self, roles):
        return self.request.user.is_staff or has_any_role(self.request.user, roles)

    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        if not self.has_permission_for([
            UserRoleAssignment.Role.TREASURER,
            UserRoleAssignment.Role.PRESIDENT,
            UserRoleAssignment.Role.VICE_PRESIDENT,
        ]):
            raise PermissionDenied("هذه السجلات متاحة لمسؤول الصندوق والرئيس ونائب الرئيس فقط.")

    def get_queryset(self):
        return FinanceTransaction.objects.select_related("created_by", "reviewed_by")

    def perform_create(self, serializer):
        if not self.has_permission_for([UserRoleAssignment.Role.TREASURER]):
            raise PermissionDenied("إنشاء المعاملات من صلاحية مسؤول الصندوق فقط.")
        serializer.save(created_by=self.request.user)

    def update(self, request, *args, **kwargs):
        raise PermissionDenied("المعاملة المالية بعد تسجيلها لا تُعدّل؛ أنشئوا معاملة تصحيحية موثقة.")

    partial_update = update

    def destroy(self, request, *args, **kwargs):
        raise PermissionDenied("لا تحذفوا السجلات المالية؛ استخدموا حالة الرفض مع توضيح السبب.")

    def decide(self, request, decision):
        if not self.has_permission_for([UserRoleAssignment.Role.PRESIDENT, UserRoleAssignment.Role.VICE_PRESIDENT]):
            raise PermissionDenied("الاعتماد المالي من صلاحية الرئيس أو نائب الرئيس.")
        item = self.get_object()
        if item.status != FinanceTransaction.Status.PENDING:
            return Response({"detail": "تمت مراجعة هذه المعاملة مسبقاً."}, status=status.HTTP_409_CONFLICT)
        if item.created_by_id == request.user.id:
            raise PermissionDenied("لا يمكن لصاحب المعاملة اعتمادها بنفسه.")
        serializer = FinanceDecisionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item.status = decision
        item.reviewed_by = request.user
        item.review_note = serializer.validated_data.get("note", "")
        item.reviewed_at = timezone.now()
        item.save(update_fields=["status", "reviewed_by", "review_note", "reviewed_at"])
        return Response(self.get_serializer(item).data)

    @action(detail=True, methods=["post"])
    @transaction.atomic
    def approve(self, request, pk=None):
        return self.decide(request, FinanceTransaction.Status.APPROVED)

    @action(detail=True, methods=["post"])
    @transaction.atomic
    def reject(self, request, pk=None):
        return self.decide(request, FinanceTransaction.Status.REJECTED)
