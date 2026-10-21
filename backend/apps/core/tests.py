from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Profile

class RegistrationRequestTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_registration_creates_pending_disabled_account_and_does_not_grant_roles(self):
        response = self.client.post("/api/auth/register/", {
            "username": "student-one", "email": "student@example.test", "password": "safe-password-123",
            "first_name": "طالب", "last_name": "تجريبي", "university_id": "20260001",
            "requested_role": "president",
        }, format="json")
        self.assertEqual(response.status_code, 201)
        user = get_user_model().objects.get(username="student-one")
        self.assertFalse(user.is_active)
        self.assertEqual(user.profile.status, Profile.Status.PENDING)
        self.assertEqual(user.profile.requested_role, Profile.RequestedRole.PRESIDENT)
        self.assertFalse(hasattr(user, "committee_memberships") and user.committee_memberships.exists())

    def test_volunteer_must_request_a_committee(self):
        response = self.client.post("/api/auth/register/", {
            "username": "student-two", "email": "two@example.test", "password": "safe-password-123",
            "first_name": "طالب", "university_id": "20260002", "requested_role": "volunteer",
        }, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(get_user_model().objects.filter(username="student-two").exists())
