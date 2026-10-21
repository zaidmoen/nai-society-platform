from django.contrib import admin
from .models import FinanceTransaction

@admin.register(FinanceTransaction)
class FinanceTransactionAdmin(admin.ModelAdmin):
    list_display = ("incurred_on", "kind", "category", "amount", "currency", "status", "created_by", "reviewed_by")
    list_filter = ("kind", "status", "currency", "category")
    search_fields = ("description", "reference", "created_by__username")
    readonly_fields = ("created_by", "reviewed_by", "reviewed_at", "created_at")
