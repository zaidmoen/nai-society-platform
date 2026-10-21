from django.db import transaction
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from apps.committees.models import CommitteeMembership
from apps.core.access import can_manage_all_committees, leads_committee
from .models import Availability, Event, EventShift
from .serializers import AvailabilitySerializer, EventSerializer

class EventViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        queryset = Event.objects.select_related("committee").prefetch_related("shifts__availability")
        user = self.request.user
        if not user.is_authenticated:
            return queryset.filter(status=Event.Status.PUBLISHED)
        if can_manage_all_committees(user):
            return queryset
        lead_ids = user.committee_memberships.filter(role=CommitteeMembership.Role.LEAD, status=CommitteeMembership.Status.ACTIVE).values_list("committee_id", flat=True)
        return queryset.filter(status=Event.Status.PUBLISHED) | queryset.filter(committee_id__in=lead_ids)

class AvailabilityViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = AvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Availability.objects.select_related("shift", "volunteer")
        if can_manage_all_committees(user):
            return Availability.objects.select_related("shift", "volunteer")
        lead_committee_ids = user.committee_memberships.filter(role=CommitteeMembership.Role.LEAD, status=CommitteeMembership.Status.ACTIVE).values_list("committee_id", flat=True)
        return Availability.objects.filter(volunteer=user) | Availability.objects.filter(shift__event__committee_id__in=lead_committee_ids)
    def perform_create(self, serializer):
        shift = serializer.validated_data["shift"]
        member = self.request.user.committee_memberships.filter(
            committee=shift.event.committee, role=CommitteeMembership.Role.VOLUNTEER,
            status=CommitteeMembership.Status.ACTIVE,
        ).exists()
        if not member:
            raise PermissionDenied("يجب أن تكون متطوعاً نشطاً في لجنة الفعالية لإرسال التوفر.")
        if shift.event.status != Event.Status.PUBLISHED:
            raise PermissionDenied("التوفر متاح للفعاليات المنشورة فقط.")
        serializer.save(volunteer=self.request.user)
    def perform_update(self, serializer):
        if serializer.instance.volunteer_id != self.request.user.id:
            raise PermissionDenied("يمكن للمتطوع تعديل أوقات توفره فقط.")
        if serializer.instance.status == Availability.Status.CONFIRMED:
            raise PermissionDenied("الفترة المؤكدة لا يغيّرها إلا منسق الفعالية.")
        if serializer.validated_data.get("shift", serializer.instance.shift) != serializer.instance.shift:
            raise PermissionDenied("لا يمكن نقل طلب التوفر إلى فترة أخرى.")
        serializer.save(volunteer=self.request.user)

    @action(detail=True, methods=["post"])
    @transaction.atomic
    def confirm(self, request, pk=None):
        availability = self.get_object()
        if not can_manage_all_committees(request.user) and not leads_committee(request.user, availability.shift.event.committee):
            raise PermissionDenied("تأكيد الفترات من صلاحية مسؤول اللجنة أو إدارة المتطوعين.")
        shift = availability.shift
        EventShift.objects.select_for_update().get(pk=shift.pk)
        if availability.status == Availability.Status.DECLINED:
            return Response({"detail": "المتطوع حدّد هذه الفترة كغير متاح."}, status=status.HTTP_400_BAD_REQUEST)
        confirmed = Availability.objects.filter(shift=shift, status=Availability.Status.CONFIRMED).exclude(pk=availability.pk).count()
        if confirmed >= shift.volunteers_needed:
            return Response({"detail": "اكتمل العدد المطلوب لهذه الفترة."}, status=status.HTTP_409_CONFLICT)
        overlapping = Availability.objects.filter(
            volunteer=availability.volunteer, status=Availability.Status.CONFIRMED,
            shift__starts_at__lt=shift.ends_at, shift__ends_at__gt=shift.starts_at,
        ).exclude(pk=availability.pk).exists()
        if overlapping:
            return Response({"detail": "لدى هذا المتطوع فترة مؤكدة تتداخل مع الوقت المحدد."}, status=status.HTTP_409_CONFLICT)
        availability.status = Availability.Status.CONFIRMED
        availability.save(update_fields=["status", "updated_at"])
        return Response(self.get_serializer(availability).data)
