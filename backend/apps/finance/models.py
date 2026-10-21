from django.conf import settings
from django.db import models

class FinanceTransaction(models.Model):
    class Kind(models.TextChoices):
        INCOME = "income", "إيراد"
        EXPENSE = "expense", "مصروف"

    class Status(models.TextChoices):
        PENDING = "pending", "بانتظار الاعتماد"
        APPROVED = "approved", "معتمد"
        REJECTED = "rejected", "مرفوض"

    kind = models.CharField(max_length=8, choices=Kind.choices)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="ILS")
    category = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    incurred_on = models.DateField()
    reference = models.CharField(max_length=180, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="finance_transactions_created")
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT, related_name="finance_transactions_reviewed")
    review_note = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-incurred_on", "-created_at"]

    def __str__(self):
        return f"{self.get_kind_display()} · {self.amount} {self.currency}"
