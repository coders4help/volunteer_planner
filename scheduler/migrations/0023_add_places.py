# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.text import slugify


def add_places(apps, schema_editor):
    countryModel = apps.get_model('places', 'Country')
    regionModel = apps.get_model('places', 'Region')
    areaModel = apps.get_model('places', 'Area')
    placeModel = apps.get_model('places', 'Place')
    locationModel = apps.get_model('scheduler', 'Location')

    germany, _ = countryModel.objects.get_or_create(name='Deutschland',
                                               defaults=dict(slug=slugify('Deutschland')))

    for location in locationModel.objects.all():

        city = location.city
        region, _ = regionModel.objects.get_or_create(name=city,
                                                 defaults=dict(slug=slugify(city),
                                                               country=germany))
        area, _ = areaModel.objects.get_or_create(name=city,
                                             defaults=dict(slug=slugify(city),
                                                           region=region))
        place, _ = placeModel.objects.get_or_create(name=city,
                                               defaults=dict(slug=slugify(city),
                                                             area=area))

        location.place = place

        location.save()


def remove_places(apps, schema_editor):
    locationModel = apps.get_model('scheduler', 'Location')
    for location in locationModel.objects.all():
        location.city = location.place.name


class Migration(migrations.Migration):
    dependencies = [
        ('scheduler', '0022_auto_20150923_1705'),
        ('places', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='location',
            options={'ordering': ('place', 'name'),
                     'verbose_name': 'location',
                     'verbose_name_plural': 'locations',
                     'permissions': (('can_view', 'User can view location'),)},
        ),
        migrations.AddField(
            model_name='location',
            name='place',
            field=models.ForeignKey(related_name='locations',
                                    verbose_name='place',
                                    to='places.Place', null=True),
        ),
        migrations.RunPython(add_places, remove_places),
        migrations.AlterField(
            model_name='location',
            name='place',
            field=models.ForeignKey(related_name='locations',
                                    verbose_name='place',
                                    to='places.Place'),
        ),
    ]
