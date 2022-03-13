from django.conf import settings

# provide sane default group names, change in settings
FACILITY_MANAGER_GROUPNAME = getattr(settings, "FACILITY_MANAGER_GROUPNAME", "Facility Manager")
ORGANIZATION_MANAGER_GROUPNAME = getattr(settings, "ORGANIZATION_MANAGER_GROUPNAME", "Organization Manager")
