from django.contrib import admin
from .models import Committee, CommitteeMembership

class MembershipInline(admin.TabularInline):
    model = CommitteeMembership
    extra = 0

@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [MembershipInline]

@admin.register(CommitteeMembership)
class CommitteeMembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "committee", "role", "status", "joined_at")
    list_filter = ("committee", "role", "status")
    search_fields = ("user__username", "user__first_name", "user__last_name")
