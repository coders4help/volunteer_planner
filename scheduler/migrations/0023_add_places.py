from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.text import slugify


def add_places(apps, schema_editor):
    country_model = apps.get_model("places", "Country")
    region_model = apps.get_model("places", "Region")
    area_model = apps.get_model("places", "Area")
    place_model = apps.get_model("places", "Place")
    location_model = apps.get_model("scheduler", "Location")

    germany, _ = country_model.objects.get_or_create(
        name="Deutschland",
        defaults={
            "slug": slugify("Deutschland"),
        },
    )

    for location in location_model.objects.all():
        city = location.city
        region, _ = region_model.objects.get_or_create(
            name=city,
            defaults={
                "slug": slugify(city),
                "country": germany,
            },
        )
        area, _ = area_model.objects.get_or_create(
            name=city,
            defaults={
                "slug": slugify(city),
                "region": region,
            },
        )
        place, _ = place_model.objects.get_or_create(
            name=city,
            defaults={
                "slug": slugify(city),
                "area": area,
            },
        )

        location.place = place

        location.save()


def remove_places(apps, schema_editor):
    location_model = apps.get_model("scheduler", "Location")
    for location in location_model.objects.all():
        location.city = location.place.name


class Migration(migrations.Migration):
    dependencies = [
        ("scheduler", "0022_auto_20150923_1705"),
        ("places", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="location",
            options={
                "ordering": ("place", "name"),
                "verbose_name": "location",
                "verbose_name_plural": "locations",
                "permissions": (("can_view", "User can view location"),),
            },
        ),
        migrations.AddField(
            model_name="location",
            name="place",
            field=models.ForeignKey(
                related_name="locations",
                verbose_name="place",
                to="places.Place",
                null=True,
                on_delete=models.SET_NULL,
            ),
        ),
        migrations.RunPython(add_places, remove_places),
        migrations.AlterField(
            model_name="location",
            name="place",
            field=models.ForeignKey(
                related_name="locations",
                verbose_name="place",
                to="places.Place",
                on_delete=models.CASCADE,
            ),
        ),
    ]
