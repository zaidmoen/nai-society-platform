from rest_framework import serializers
from .models import FinanceTransaction

class FinanceTransactionSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source="created_by.get_full_name", read_only=True)
    reviewed_by_name = serializers.CharField(source="reviewed_by.get_full_name", read_only=True)
    class Meta:
        model = FinanceTransaction
        fields = ["id", "kind", "status", "amount", "currency", "category", "description", "incurred_on", "reference", "created_by", "created_by_name", "reviewed_by", "reviewed_by_name", "review_note", "created_at", "reviewed_at"]
        read_only_fields = ["id", "status", "created_by", "created_by_name", "reviewed_by", "reviewed_by_name", "review_note", "created_at", "reviewed_at"]

class FinanceDecisionSerializer(serializers.Serializer):
    note = serializers.CharField(max_length=500, required=False, allow_blank=True)
