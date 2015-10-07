# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def needs_to_shifts(apps, schema_editor):
    Need = apps.get_model('scheduler', 'Need')
    Shift = apps.get_model('scheduler', 'Shift')
    Workplace = apps.get_model('organizations', 'Workplace')
    Task = apps.get_model('organizations', 'Task')

    for need in Need.objects.all():
        shift = Shift()
        shift.facility = need.facility
        shift.needed_volunteers = need.slots
        shift.start_time = need.starting_time
        shift.end_time = need.ending_time
        shift.workplace, _ = Workplace.objects.get_or_create(
            facility=need.facility,
            name='default workplace',
            defaults=dict(description=need.topic.description)
        )
        shift.task, _ = Task.objects.get_or_create(facility=need.facility,
                                                   name=need.topic.title,
                                                   defaults=dict(
                                                       description=need.topic.description))
        shift.save()


def skip(apps, schema_editor):
    Shift = apps.get_model('scheduler', 'Shift')
    Workplace = apps.get_model('organizations', 'Workplace')
    Task = apps.get_model('organizations', 'Task')

    Shift.objects.all().delete()
    Workplace.objects.all().delete()
    Task.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('scheduler', '0029_auto_20151006_1752'),
    ]

    operations = [
        migrations.RunPython(needs_to_shifts, skip)
    ]
