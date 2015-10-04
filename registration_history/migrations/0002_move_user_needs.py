# coding: utf-8

from __future__ import unicode_literals

import sys

from django.db import migrations

ACTIVATED = u"ALREADY_ACTIVATED"


def move_user_needs(apps, schema_editor):
    OldRegistrationModel = apps.get_model("registration_history",
                                          'OldRegistrationProfile')
    UserAccount = apps.get_model("accounts", "UserAccount")
    ShiftHelper = apps.get_model("scheduler", "ShiftHelper")

    sys.stdout.write(' ' * 80)
    sys.stdout.flush()

    account_count, shift_count, users_without_shifts = 0, 0, 0
    for rp in OldRegistrationModel.objects.all():

        if rp.activation_key == ACTIVATED:
            has_shifts = False
            account, _ = UserAccount.objects.get_or_create(user=rp.user)
            account_count += 1
            for need in rp.needs.all():
                shift_helper, _ = ShiftHelper.objects.get_or_create(
                    user_account=account, need=need)
                shift_count += 1
                has_shifts = True
            if not has_shifts:
                users_without_shifts += 1
        if account_count % 43 == 0:
            sys.stdout.write(
                '\r    Migrated {} accounts totalling {} shifts ({} users w/o shifts)'.format(
                    account_count, shift_count, users_without_shifts))
            sys.stdout.flush()


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
        ('registration_history', '0001_initial'),
        ('scheduler', '0021_add_shift_users'),
    ]

    operations = [
        migrations.RunPython(move_user_needs)
    ]
