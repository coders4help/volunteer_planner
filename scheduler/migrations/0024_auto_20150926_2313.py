from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scheduler", "0023_add_places"),
    ]

    operations = [
        migrations.AlterField(
            model_name="location",
            name="additional_info",
            field=models.TextField(
                max_length=300000, verbose_name="description", blank=True
            ),
        ),
        migrations.AlterField(
            model_name="location",
            name="city",
            field=models.CharField(max_length=255, verbose_name="city", blank=True),
        ),
        migrations.AlterField(
            model_name="location",
            name="latitude",
            field=models.CharField(max_length=30, verbose_name="latitude", blank=True),
        ),
        migrations.AlterField(
            model_name="location",
            name="longitude",
            field=models.CharField(max_length=30, verbose_name="longitude", blank=True),
        ),
        migrations.AlterField(
            model_name="location",
            name="name",
            field=models.CharField(max_length=255, verbose_name="name", blank=True),
        ),
        migrations.AlterField(
            model_name="location",
            name="postal_code",
            field=models.CharField(
                max_length=5, verbose_name="postal code", blank=True
            ),
        ),
        migrations.AlterField(
            model_name="location",
            name="street",
            field=models.CharField(max_length=255, verbose_name="address", blank=True),
        ),
    ]
