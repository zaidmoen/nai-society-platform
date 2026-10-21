from datetime import date
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from apps.core.models import UserRoleAssignment
from .models import FinanceTransaction

class FinanceApprovalTests(TestCase):
    def setUp(self):
        self.treasurer = get_user_model().objects.create_user(username="treasurer", password="secure-password-123", is_active=True)
        self.president = get_user_model().objects.create_user(username="president", password="secure-password-123", is_active=True)
        UserRoleAssignment.objects.create(user=self.treasurer, role=UserRoleAssignment.Role.TREASURER)
        UserRoleAssignment.objects.create(user=self.president, role=UserRoleAssignment.Role.PRESIDENT)
        self.client = APIClient()

    def test_treasurer_creates_pending_record_and_president_approves(self):
        self.client.force_authenticate(self.treasurer)
        created = self.client.post("/api/finance/transactions/", {
            "kind": "expense", "amount": "25.00", "currency": "ILS", "category": "supplies",
            "description": "Demo transaction", "incurred_on": date.today().isoformat(),
        }, format="json")
        self.assertEqual(created.status_code, 201)
        transaction = FinanceTransaction.objects.get()
        self.assertEqual(transaction.status, FinanceTransaction.Status.PENDING)
        self.client.force_authenticate(self.president)
        approved = self.client.post(f"/api/finance/transactions/{transaction.id}/approve/", {"note": "Reviewed"}, format="json")
        self.assertEqual(approved.status_code, 200)
        transaction.refresh_from_db()
        self.assertEqual(transaction.status, FinanceTransaction.Status.APPROVED)
        self.assertEqual(transaction.reviewed_by, self.president)

    def test_creator_cannot_approve_own_transaction(self):
        UserRoleAssignment.objects.create(user=self.treasurer, role=UserRoleAssignment.Role.PRESIDENT)
        item = FinanceTransaction.objects.create(
            kind="income", amount="100.00", category="support", description="Demo",
            incurred_on=date.today(), created_by=self.treasurer,
        )
        self.client.force_authenticate(self.treasurer)
        response = self.client.post(f"/api/finance/transactions/{item.id}/approve/", {}, format="json")
        self.assertEqual(response.status_code, 403)
        item.refresh_from_db()
        self.assertEqual(item.status, FinanceTransaction.Status.PENDING)
