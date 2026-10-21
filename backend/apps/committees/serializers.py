from rest_framework import serializers
from .models import Committee, CommitteeMembership

class CommitteeMembershipSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.get_full_name", read_only=True)
    class Meta:
        model = CommitteeMembership
        fields = ["id", "name", "role", "status", "joined_at"]

class CommitteeSerializer(serializers.ModelSerializer):
    volunteers_count = serializers.SerializerMethodField()
    class Meta:
        model = Committee
        fields = ["id", "name", "slug", "description", "volunteers_count"]
    def get_volunteers_count(self, obj):
        return obj.memberships.filter(status=CommitteeMembership.Status.ACTIVE).count()
