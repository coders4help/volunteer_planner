"""

Removes field `short_description` from models Organization and Facility.

If short_description is not empty, it copies it's content of Organization
and Facility model to beginning of its description field.

"""

from django.db import migrations


def combine_descriptions(apps, schema_editor):

    models = (
        apps.get_model("organizations", "Organization"),
        apps.get_model("organizations", "Facility"),
    )

    for Model in models:
        for object in Model.objects.exclude(short_description="").exclude(short_description=None):
            short_description = (object.short_description or "").strip()
            if short_description:
                description = (object.description or "").strip()
                object.description = f"{short_description}\n\n\n{description}\n".strip()
                object.save()


class Migration(migrations.Migration):

    dependencies = [
        ("organizations", "0013_add_manager_group_permissions"),
    ]

    operations = [
        migrations.RunPython(combine_descriptions, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="facility",
            name="short_description",
        ),
        migrations.RemoveField(
            model_name="organization",
            name="short_description",
        ),
    ]
