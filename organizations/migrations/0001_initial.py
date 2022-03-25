# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("places", "0002_auto_20150926_2313"),
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Facility",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("name", models.CharField(max_length=256, verbose_name="name")),
                (
                    "short_description",
                    models.TextField(verbose_name="short description", blank=True),
                ),
                ("description", models.TextField(verbose_name="description")),
                ("contact_info", models.TextField(verbose_name="description")),
                ("address", models.TextField(verbose_name="address")),
                (
                    "zip_code",
                    models.CharField(
                        max_length=25, verbose_name="postal code", blank=True
                    ),
                ),
                (
                    "show_on_map",
                    models.BooleanField(
                        default=True, verbose_name="Show on map of all facilities"
                    ),
                ),
                (
                    "latitude",
                    models.CharField(
                        max_length=30, verbose_name="latitude", blank=True
                    ),
                ),
                (
                    "longitude",
                    models.CharField(
                        max_length=30, verbose_name="longitude", blank=True
                    ),
                ),
            ],
            options={
                "ordering": ("organization", "place", "name"),
                "verbose_name": "facility",
                "verbose_name_plural": "facilities",
            },
        ),
        migrations.CreateModel(
            name="FacilityMembership",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "role",
                    models.PositiveIntegerField(
                        default=2,
                        verbose_name="role",
                        choices=[(0, "Admin"), (1, "Manager"), (2, "Member")],
                    ),
                ),
                (
                    "facility",
                    models.ForeignKey(
                        related_name="memberships",
                        verbose_name="facility",
                        to="organizations.Facility",
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "user_account",
                    models.ForeignKey(
                        verbose_name="user account",
                        to="accounts.UserAccount",
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={
                "ordering": ("facility", "role", "user_account"),
                "verbose_name": "facility member",
                "verbose_name_plural": "facility members",
            },
        ),
        migrations.CreateModel(
            name="Organization",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("name", models.CharField(max_length=256, verbose_name="name")),
                (
                    "short_description",
                    models.TextField(verbose_name="short description", blank=True),
                ),
                ("description", models.TextField(verbose_name="description")),
                ("contact_info", models.TextField(verbose_name="description")),
                ("address", models.TextField(verbose_name="address")),
            ],
            options={
                "ordering": ("name",),
                "verbose_name": "organization",
                "verbose_name_plural": "organizations",
            },
        ),
        migrations.CreateModel(
            name="OrganizationMembership",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "role",
                    models.PositiveIntegerField(
                        default=2,
                        verbose_name="role",
                        choices=[(0, "Admin"), (1, "Manager"), (2, "Member")],
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        related_name="memberships",
                        verbose_name="organization",
                        to="organizations.Organization",
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "user_account",
                    models.ForeignKey(
                        verbose_name="user account",
                        to="accounts.UserAccount",
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={
                "ordering": ("organization", "role", "user_account"),
                "verbose_name": "organization member",
                "verbose_name_plural": "organization members",
            },
        ),
        migrations.AddField(
            model_name="organization",
            name="members",
            field=models.ManyToManyField(
                to="accounts.UserAccount",
                through="organizations.OrganizationMembership",
            ),
        ),
        migrations.AddField(
            model_name="facility",
            name="members",
            field=models.ManyToManyField(
                to="accounts.UserAccount", through="organizations.FacilityMembership"
            ),
        ),
        migrations.AddField(
            model_name="facility",
            name="organization",
            field=models.ForeignKey(
                related_name="facilities",
                verbose_name="organization",
                to="organizations.Organization",
                on_delete=models.CASCADE,
            ),
        ),
        migrations.AddField(
            model_name="facility",
            name="place",
            field=models.ForeignKey(
                related_name="facilities",
                verbose_name="place",
                to="places.Place",
                on_delete=models.CASCADE,
            ),
        ),
    ]
