from rest_framework import permissions, viewsets
from apps.committees.models import CommitteeMembership
from apps.core.access import can_manage_all_committees, leads_committee
from .models import CommitteeNote, Evaluation
from .serializers import CommitteeNoteSerializer, EvaluationSerializer

class IsCommitteeLeadOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and (can_manage_all_committees(request.user) or request.user.committee_memberships.filter(role=CommitteeMembership.Role.LEAD, status=CommitteeMembership.Status.ACTIVE).exists())

class EvaluationViewSet(viewsets.ModelViewSet):
    serializer_class = EvaluationSerializer
    permission_classes = [IsCommitteeLeadOrAdmin]
    def get_queryset(self):
        user = self.request.user
        queryset = Evaluation.objects.select_related("committee", "volunteer", "evaluator", "participation")
        if can_manage_all_committees(user):
            return queryset
        committee_ids = user.committee_memberships.filter(role=CommitteeMembership.Role.LEAD, status=CommitteeMembership.Status.ACTIVE).values_list("committee_id", flat=True)
        return queryset.filter(committee_id__in=committee_ids) | queryset.filter(volunteer=user, status=Evaluation.Status.PUBLISHED)
    def perform_create(self, serializer):
        committee = serializer.validated_data["committee"]
        if not can_manage_all_committees(self.request.user) and not leads_committee(self.request.user, committee):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("يمكن لمسؤول اللجنة تقييم متطوعي لجنته فقط.")
        serializer.save(evaluator=self.request.user)

class CommitteeNoteViewSet(viewsets.ModelViewSet):
    serializer_class = CommitteeNoteSerializer
    permission_classes = [IsCommitteeLeadOrAdmin]
    def get_queryset(self):
        user = self.request.user
        queryset = CommitteeNote.objects.select_related("committee", "volunteer", "author", "participation")
        if can_manage_all_committees(user):
            return queryset
        committee_ids = user.committee_memberships.filter(role=CommitteeMembership.Role.LEAD, status=CommitteeMembership.Status.ACTIVE).values_list("committee_id", flat=True)
        return queryset.filter(committee_id__in=committee_ids) | queryset.filter(volunteer=user, visibility=CommitteeNote.Visibility.SHARED)
    def perform_create(self, serializer):
        committee = serializer.validated_data["committee"]
        if not can_manage_all_committees(self.request.user) and not leads_committee(self.request.user, committee):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("يمكن لمسؤول اللجنة إضافة ملاحظات ضمن لجنته فقط.")
        serializer.save(author=self.request.user)
