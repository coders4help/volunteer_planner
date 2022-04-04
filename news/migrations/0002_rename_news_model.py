# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("organizations", "0007_auto_20151023_2129"),
        ("news", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(old_name="News", new_name="NewsEntry"),
        migrations.AlterModelOptions(
            name="newsentry",
            options={
                "ordering": ("facility", "organization", "creation_date"),
                "verbose_name": "news entry",
                "verbose_name_plural": "news entries",
            },
        ),
        migrations.AlterField(
            model_name="newsentry",
            name="facility",
            field=models.ForeignKey(
                related_name="news_entries",
                blank=True,
                to="organizations.Facility",
                null=True,
                on_delete=models.SET_NULL,
            ),
        ),
        migrations.AlterField(
            model_name="newsentry",
            name="organization",
            field=models.ForeignKey(
                related_name="news_entries",
                blank=True,
                to="organizations.Organization",
                null=True,
                on_delete=models.SET_NULL,
            ),
        ),
        migrations.AlterField(
            model_name="newsentry",
            name="text",
            field=models.TextField(verbose_name="articletext"),
        ),
    ]
