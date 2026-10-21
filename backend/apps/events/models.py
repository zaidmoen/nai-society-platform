from django.conf import settings
from django.db import models
from apps.committees.models import Committee

class Event(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "مسودة"
        REVIEW = "review", "بانتظار المراجعة"
        PUBLISHED = "published", "منشور"
        COMPLETED = "completed", "منتهٍ"
        CANCELLED = "cancelled", "ملغي"

    title = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    committee = models.ForeignKey(Committee, on_delete=models.PROTECT, related_name="events")
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    location = models.CharField(max_length=180, blank=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.DRAFT)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="created_events")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["starts_at"]

    def __str__(self):
        return self.title

class EventShift(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="shifts")
    title = models.CharField(max_length=120)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    volunteers_needed = models.PositiveSmallIntegerField(default=1)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["position", "starts_at"]

    def __str__(self):
        return f"{self.event}: {self.title}"

class Availability(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "available", "متاح"
        CONFIRMED = "confirmed", "مؤكد"
        DECLINED = "declined", "غير متاح"

    shift = models.ForeignKey(EventShift, on_delete=models.CASCADE, related_name="availability")
    volunteer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="event_availability")
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.AVAILABLE)
    note = models.CharField(max_length=300, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["shift", "volunteer"], name="unique_volunteer_shift_availability")]

class Attendance(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="attendance")
    volunteer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="event_attendance")
    shift = models.ForeignKey(EventShift, null=True, blank=True, on_delete=models.SET_NULL, related_name="attendance")
    attended = models.BooleanField(default=False)
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="attendance_records_created")
    recorded_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["event", "volunteer"], name="unique_event_volunteer_attendance")]
