from rest_framework import viewsets
from .models import Committee
from .serializers import CommitteeSerializer

class CommitteeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Committee.objects.filter(is_active=True).prefetch_related("memberships")
    serializer_class = CommitteeSerializer
