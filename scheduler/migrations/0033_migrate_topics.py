# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def migrate_topics(apps, schema_editor):
    Shift = apps.get_model('scheduler', 'Shift')
    Workplace = apps.get_model('organizations', 'Workplace')
    Task = apps.get_model('organizations', 'Task')

    for shift in Shift.objects.select_related('topic', 'facility'):
        facility = shift.facility
        topic = shift.topic

        if shift.topic.workplace:
            workplace, _ = Workplace.objects.get_or_create(
                facility=facility,
                name=topic.workplace)
            shift.workplace = workplace

        defaults = dict(description=topic.description)
        task, _ = Task.objects.get_or_create(facility=facility,
                                             name=topic.title,
                                             defaults=defaults)
        shift.task = task
        shift.save()

def skip(_, __):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('scheduler', '0032_add_task_and_workplace_to_shift'),
    ]

    operations = [
        migrations.RunPython(migrate_topics, skip)
    ]
