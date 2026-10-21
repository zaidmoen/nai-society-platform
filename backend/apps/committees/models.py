from django.conf import settings
from django.db import models

class Committee(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class CommitteeMembership(models.Model):
    class Role(models.TextChoices):
        VOLUNTEER = "volunteer", "متطوع"
        LEAD = "lead", "مسؤول لجنة"

    class Status(models.TextChoices):
        ACTIVE = "active", "نشط"
        PAUSED = "paused", "متوقف مؤقتاً"
        ENDED = "ended", "منتهٍ"

    committee = models.ForeignKey(Committee, on_delete=models.PROTECT, related_name="memberships")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="committee_memberships")
    role = models.CharField(max_length=12, choices=Role.choices, default=Role.VOLUNTEER)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.ACTIVE)
    joined_at = models.DateField(null=True, blank=True)
    ended_at = models.DateField(null=True, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["committee", "user"], name="unique_committee_member")]

    def __str__(self):
        return f"{self.user} — {self.committee}"
