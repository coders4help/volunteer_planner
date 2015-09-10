# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

# This migration is manually created to convert the 'needs' M2M to the 'shifts' M2M, because the second has a through field and auto conversion is otherwise not possible.
class Migration(migrations.Migration):

    def needs_to_shifts(apps, schema_editor):
        RegistrationProfile = apps.get_model("registration", "RegistrationProfile")
        scheduledRegPro = apps.get_model("scheduler", "scheduledRegPro")

        for reg_pro in RegistrationProfile.objects.all():
            for need in reg_pro.needs.all():
                srp = scheduledRegPro(
                need = need,
                registration_profile = reg_pro
                )
                srp.save()


    dependencies = [
        ('registration', '0006_auto_20150910_2123'),
    ]

    operations = [
        migrations.RunPython(needs_to_shifts),
    ]
