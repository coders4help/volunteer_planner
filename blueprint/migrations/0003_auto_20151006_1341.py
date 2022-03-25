# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blueprint", "0002_needblueprint_slots"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="blueprintcreator",
            options={"verbose_name": "Blueprint", "verbose_name_plural": "Blueprints"},
        ),
        migrations.AlterModelOptions(
            name="needblueprint",
            options={
                "verbose_name": "Blueprint Item",
                "verbose_name_plural": "Blueprint Items",
            },
        ),
        migrations.AlterField(
            model_name="blueprintcreator",
            name="location",
            field=models.ForeignKey(
                verbose_name="location",
                to="scheduler.Location",
                on_delete=models.CASCADE,
            ),
        ),
        migrations.AlterField(
            model_name="blueprintcreator",
            name="needs",
            field=models.ManyToManyField(
                to="blueprint.NeedBluePrint", verbose_name="shifts"
            ),
        ),
        migrations.AlterField(
            model_name="blueprintcreator",
            name="title",
            field=models.CharField(max_length=255, verbose_name="blueprint title"),
        ),
        migrations.AlterField(
            model_name="needblueprint",
            name="from_time",
            field=models.CharField(max_length=5, verbose_name="from hh:mm"),
        ),
        migrations.AlterField(
            model_name="needblueprint",
            name="slots",
            field=models.IntegerField(verbose_name="number of volunteers needed"),
        ),
        migrations.AlterField(
            model_name="needblueprint",
            name="to_time",
            field=models.CharField(max_length=5, verbose_name="until hh:mm"),
        ),
        migrations.AlterField(
            model_name="needblueprint",
            name="topic",
            field=models.ForeignKey(
                verbose_name="topic", to="scheduler.Topics", on_delete=models.CASCADE
            ),
        ),
    ]
