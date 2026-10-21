from rest_framework import serializers
from .models import CommitteeNote, Evaluation

class EvaluationSerializer(serializers.ModelSerializer):
    volunteer_name = serializers.CharField(source="volunteer.get_full_name", read_only=True)
    class Meta:
        model = Evaluation
        fields = ["id", "committee", "volunteer", "volunteer_name", "evaluator", "period_label", "participation", "scores", "evidence", "strength", "growth_step", "status", "volunteer_response", "created_at", "updated_at"]
        read_only_fields = ["id", "evaluator", "created_at", "updated_at"]

class CommitteeNoteSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.get_full_name", read_only=True)
    class Meta:
        model = CommitteeNote
        fields = ["id", "committee", "volunteer", "author", "author_name", "participation", "body", "visibility", "created_at"]
        read_only_fields = ["id", "author", "author_name", "created_at"]
