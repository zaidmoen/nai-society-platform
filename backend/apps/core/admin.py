from django.contrib import admin
from django.utils import timezone
from apps.committees.models import Committee, CommitteeMembership
from .models import Profile, UserRoleAssignment

@admin.action(description="اعتماد طلب الحساب والدور المطلوب")
def approve_profiles(modeladmin, request, queryset):
    approved = 0
    missing_committee = []
    for profile in queryset.select_related("user"):
        if profile.requested_role in (Profile.RequestedRole.VOLUNTEER, Profile.RequestedRole.COMMITTEE_LEAD):
            committee = Committee.objects.filter(name=profile.requested_committee, is_active=True).first()
            if committee is None:
                missing_committee.append(profile.user.get_full_name() or profile.user.username)
                continue
            membership_role = CommitteeMembership.Role.LEAD if profile.requested_role == Profile.RequestedRole.COMMITTEE_LEAD else CommitteeMembership.Role.VOLUNTEER
            CommitteeMembership.objects.update_or_create(
                committee=committee, user=profile.user,
                defaults={"role": membership_role, "status": CommitteeMembership.Status.ACTIVE},
            )
        else:
            UserRoleAssignment.objects.update_or_create(
                user=profile.user, role=profile.requested_role,
                defaults={"is_active": True, "granted_by": request.user},
            )
        profile.status = Profile.Status.ACTIVE
        profile.approved_at = timezone.now()
        profile.user.is_active = True
        profile.user.save(update_fields=["is_active"])
        profile.save(update_fields=["status", "approved_at"])
        approved += 1
    if approved:
        modeladmin.message_user(request, f"تم اعتماد {approved} حساب/دور.")
    if missing_committee:
        modeladmin.message_user(request, "تعذّر اعتماد هذه الطلبات؛ أنشئوا اللجنة المطلوبة أولاً: " + "، ".join(missing_committee), level="WARNING")

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "university_id", "requested_role", "requested_committee", "status", "created_at")
    list_filter = ("status", "requested_role")
    search_fields = ("user__username", "user__first_name", "user__last_name", "university_id")
    actions = [approve_profiles]

@admin.register(UserRoleAssignment)
class UserRoleAssignmentAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "is_active", "granted_by", "granted_at")
    list_filter = ("role", "is_active")
    search_fields = ("user__username", "user__first_name", "user__last_name")
