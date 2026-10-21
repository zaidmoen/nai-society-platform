from apps.committees.models import CommitteeMembership
from apps.core.models import UserRoleAssignment

def has_any_role(user, roles):
    if not user or not user.is_authenticated:
        return False
    return user.role_assignments.filter(role__in=roles, is_active=True).exists()

def leads_committee(user, committee):
    if not user or not user.is_authenticated:
        return False
    return user.committee_memberships.filter(
        committee=committee, role=CommitteeMembership.Role.LEAD,
        status=CommitteeMembership.Status.ACTIVE,
    ).exists()

def can_manage_all_committees(user):
    return bool(user.is_staff or has_any_role(user, [
        UserRoleAssignment.Role.PRESIDENT,
        UserRoleAssignment.Role.VICE_PRESIDENT,
        UserRoleAssignment.Role.VOLUNTEER_MANAGER,
    ]))
