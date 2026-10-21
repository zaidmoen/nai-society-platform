from datetime import timedelta
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from apps.committees.models import Committee, CommitteeMembership
from .models import Availability, Event, EventShift

class VolunteerAvailabilityTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="volunteer", password="safe-password-123")
        self.committee = Committee.objects.create(name="لجنة التقنية", slug="technology")
        start = timezone.now() + timedelta(days=1)
        self.event = Event.objects.create(title="فعالية تجريبية", committee=self.committee, starts_at=start, ends_at=start + timedelta(hours=4), created_by=self.user, status=Event.Status.PUBLISHED)
        self.shift = EventShift.objects.create(event=self.event, title="الاستقبال", starts_at=start, ends_at=start + timedelta(hours=1))
        CommitteeMembership.objects.create(committee=self.committee, user=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_volunteer_can_submit_availability_for_self(self):
        response = self.client.post("/api/availability/", {"shift": self.shift.id, "note": "متاح"}, format="json")
        self.assertEqual(response.status_code, 201)
        availability = Availability.objects.get()
        self.assertEqual(availability.volunteer, self.user)
        self.assertEqual(availability.status, Availability.Status.AVAILABLE)

    def test_volunteer_cannot_self_confirm_shift(self):
        response = self.client.post("/api/availability/", {"shift": self.shift.id, "status": "confirmed"}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Availability.objects.exists())
