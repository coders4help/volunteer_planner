# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
        ("organizations", "0004_add_tasks"),
        ("scheduler", "0030_delete_location"),
    ]

    operations = [
        migrations.RenameModel(old_name="Need", new_name="Shift"),
        migrations.AlterField(
            model_name="shifthelper",
            name="need",
            field=models.ForeignKey(
                related_name="shift_helpers",
                to="scheduler.Shift",
                on_delete=models.CASCADE,
            ),
        ),
        migrations.RenameField(
            model_name="shifthelper",
            old_name="need",
            new_name="shift",
        ),
        migrations.AlterUniqueTogether(
            name="shifthelper",
            unique_together=set([("user_account", "shift")]),
        ),
        migrations.AlterField(
            model_name="shift",
            name="helpers",
            field=models.ManyToManyField(
                related_name="shifts",
                through="scheduler.ShiftHelper",
                to="accounts.UserAccount",
            ),
        ),
    ]
