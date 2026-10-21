from django.conf import settings
from django.db import models
from apps.committees.models import Committee
from apps.events.models import Event

class Evaluation(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "مسودة"
        REVIEW = "review", "بانتظار المراجعة"
        PUBLISHED = "published", "منشور للمتطوع"

    committee = models.ForeignKey(Committee, on_delete=models.PROTECT, related_name="evaluations")
    volunteer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="evaluations_received")
    evaluator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="evaluations_written")
    period_label = models.CharField(max_length=80)
    participation = models.ForeignKey(Event, null=True, blank=True, on_delete=models.SET_NULL, related_name="evaluations")
    scores = models.JSONField(default=dict, help_text="Scores for the agreed committee evaluation criteria")
    evidence = models.TextField(blank=True)
    strength = models.TextField(blank=True)
    growth_step = models.TextField(blank=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.DRAFT)
    volunteer_response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [models.UniqueConstraint(fields=["committee", "volunteer", "period_label"], name="one_evaluation_per_committee_period")]

class CommitteeNote(models.Model):
    class Visibility(models.TextChoices):
        SHARED = "shared", "مرئية للمتطوع"
        INTERNAL = "internal", "متابعة إدارية محدودة"

    committee = models.ForeignKey(Committee, on_delete=models.PROTECT, related_name="notes")
    volunteer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="committee_notes")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="committee_notes_written")
    participation = models.ForeignKey(Event, null=True, blank=True, on_delete=models.SET_NULL, related_name="committee_notes")
    body = models.CharField(max_length=1200)
    visibility = models.CharField(max_length=10, choices=Visibility.choices, default=Visibility.SHARED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
