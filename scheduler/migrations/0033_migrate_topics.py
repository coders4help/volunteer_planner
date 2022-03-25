# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def migrate_topics(apps, schema_editor):
    shift_model = apps.get_model("scheduler", "Shift")
    workplace_model = apps.get_model("organizations", "Workplace")
    task_model = apps.get_model("organizations", "Task")

    for shift in shift_model.objects.select_related("topic", "facility"):
        facility = shift.facility
        topic = shift.topic

        if shift.topic.workplace:
            workplace, _ = workplace_model.objects.get_or_create(
                facility=facility, name=topic.workplace
            )
            shift.workplace = workplace

        defaults = dict(description=topic.description)
        task, _ = task_model.objects.get_or_create(
            facility=facility, name=topic.title, defaults=defaults
        )
        shift.task = task
        shift.save()


def skip(_, __):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("scheduler", "0032_add_task_and_workplace_to_shift"),
    ]

    operations = [migrations.RunPython(migrate_topics, skip)]
