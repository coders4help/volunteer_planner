# Generated by Django 2.2.3 on 2022-03-12 09:57

from django.db import migrations

from organizations.models import Membership
from ..settings import FACILITY_MANAGER_GROUPNAME, ORGANIZATION_MANAGER_GROUPNAME

ADD = "add"
CHANGE = "change"
DELETE = "delete"
VIEW = "view"

MANAGER_GROUPS = {
    FACILITY_MANAGER_GROUPNAME: (),
    ORGANIZATION_MANAGER_GROUPNAME: (
        ("organizations", "Organization", (ADD, CHANGE, DELETE, VIEW)),
        ("organizations", "OrganizationMembership", (ADD, CHANGE, DELETE, VIEW)),
    ),
}


def forwards(apps, schema_editor):
    ContentTypeModel = apps.get_model("contenttypes", "ContentType")
    GroupModel = apps.get_model("auth", "Group")
    PermissionModel = apps.get_model("auth", "Permission")

    for group_name, permissions in MANAGER_GROUPS.items():
        group, _ = GroupModel.objects.get_or_create(name=group_name)
        for app_label, model, actions in permissions:
            content_type = ContentTypeModel.objects.get(app_label=app_label.lower(), model=model.lower())
            for action in actions:
                permission = PermissionModel.objects.get(
                    content_type=content_type, codename=f"{action}_{model}".lower()
                )
                group.permissions.add(permission)

    OrganizationMembershipModel = apps.get_model("organizations", "OrganizationMembership")
    for organization_member in OrganizationMembershipModel.objects.filter(role__lt=Membership.Roles.MEMBER):
        organization_member.user_account.user.groups.add(GroupModel.objects.get(name=ORGANIZATION_MANAGER_GROUPNAME))

    FacilityMembershipModel = apps.get_model("organizations", "FacilityMembership")
    for facility_member in FacilityMembershipModel.objects.filter(role__lt=Membership.Roles.MEMBER):
        facility_member.user_account.user.groups.add(GroupModel.objects.get(name=FACILITY_MANAGER_GROUPNAME))


def backwards(apps, schema_editor):
    GroupModel = apps.get_model("auth", "Group")
    for group_name in MANAGER_GROUPS.keys():
        GroupModel.objects.get(name=group_name).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0011_update_proxy_permissions"),
        ("organizations", "0012_cascade_deletion"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
