from django.conf import settings
from django.db import models

class Profile(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "بانتظار التحقق"
        ACTIVE = "active", "نشط"
        PAUSED = "paused", "متوقف مؤقتاً"
        INACTIVE = "inactive", "غير نشط"

    class RequestedRole(models.TextChoices):
        MEMBER = "member", "منتسب"
        VOLUNTEER = "volunteer", "متطوع"
        COMMITTEE_LEAD = "committee_lead", "مسؤول لجنة"
        VOLUNTEER_MANAGER = "volunteer_manager", "مسؤول المتطوعين"
        VICE_PRESIDENT = "vice_president", "نائب الرئيس"
        PRESIDENT = "president", "الرئيس"
        TREASURER = "treasurer", "مسؤول الصندوق"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    university_id = models.CharField(max_length=32, blank=True, db_index=True)
    phone = models.CharField(max_length=32, blank=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
    requested_role = models.CharField(max_length=24, choices=RequestedRole.choices, default=RequestedRole.MEMBER)
    requested_committee = models.CharField(max_length=80, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class UserRoleAssignment(models.Model):
    class Role(models.TextChoices):
        MEMBER = "member", "منتسب"
        VOLUNTEER_MANAGER = "volunteer_manager", "مسؤول المتطوعين"
        VICE_PRESIDENT = "vice_president", "نائب الرئيس"
        PRESIDENT = "president", "الرئيس"
        TREASURER = "treasurer", "مسؤول الصندوق"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="role_assignments")
    role = models.CharField(max_length=24, choices=Role.choices)
    granted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="roles_granted")
    granted_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "role"], name="unique_user_global_role")]

    def __str__(self):
        return f"{self.user} — {self.get_role_display()}"
