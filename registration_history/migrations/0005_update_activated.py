# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def migrate_activated_status(apps, schema_editor):
    # We can't directly import the RegistrationProfile model
    # as it may be a different version than this migration expects.
    OldRegistrationModel = apps.get_model("registration_history",
                                          'OldRegistrationProfile')

    # Filter the queryset to only fetch already activated profiles.
    # Note, we don't use the string constant `ACTIVATED` because we are using
    # the actual model, not necessarily the Python class which has said attribute.

    OldRegistrationModel.objects.update(activated=False)
    for rp in OldRegistrationModel.objects.filter(
            activation_key='ALREADY_ACTIVATED'):
        # Note, it's impossible to get the original activation key, so just
        # leave the ALREADY_ACTIVATED string.
        rp.activated = True
        rp.save()


class Migration(migrations.Migration):
    dependencies = [
        ('registration_history', '0004_migrate_to_redux'),
    ]

    operations = [
        migrations.RunPython(migrate_activated_status)
    ]
