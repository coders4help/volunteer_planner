from __future__ import unicode_literals

import sys

from django.db import migrations, models
from django.utils.text import slugify

from common.migrations import skip


def add_slugs(apps, schema_editor):
    organization_model = apps.get_model("organizations", "Organization")
    facility_model = apps.get_model("organizations", "Facility")

    for model in (organization_model, facility_model):
        for instance in model.objects.all():
            instance.slug = slugify(instance.name)[:80] or slugify(
                "{}".format(instance.id)
            )
            instance.save()
            sys.stdout.write("{} -> {}\n".format(instance, instance.slug))


class Migration(migrations.Migration):
    dependencies = [
        ("organizations", "0007_auto_20151023_2129"),
    ]

    operations = [
        migrations.AddField(
            model_name="facility",
            name="slug",
            field=models.SlugField(
                max_length=80, null=True, verbose_name="slug", blank=True
            ),
        ),
        migrations.AddField(
            model_name="organization",
            name="slug",
            field=models.SlugField(
                max_length=80, null=True, verbose_name="slug", blank=True
            ),
        ),
        migrations.RunPython(add_slugs, skip),
        migrations.AlterField(
            model_name="facility",
            name="slug",
            field=models.SlugField(max_length=80, verbose_name="slug"),
        ),
        migrations.AlterField(
            model_name="organization",
            name="slug",
            field=models.SlugField(max_length=80, verbose_name="slug"),
        ),
    ]
