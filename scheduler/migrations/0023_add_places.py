# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.text import slugify


def add_places(apps, schema_editor):
    Country = apps.get_model('places', 'Country')
    Region = apps.get_model('places', 'Region')
    Area = apps.get_model('places', 'Area')
    Place = apps.get_model('places', 'Place')
    Location = apps.get_model('scheduler', 'Location')

    germany, _ = Country.objects.get_or_create(name='Deutschland',
                                               defaults=dict(slug=slugify('Deutschland')))

    for location in Location.objects.all():

        city = location.city
        region, _ = Region.objects.get_or_create(name=city,
                                                 defaults=dict(slug=slugify(city),
                                                               country=germany))
        area, _ = Area.objects.get_or_create(name=city,
                                             defaults=dict(slug=slugify(city),
                                                           region=region))
        place, _ = Place.objects.get_or_create(name=city,
                                               defaults=dict(slug=slugify(city),
                                                             area=area))

        location.place = place

        location.save()


def remove_places(apps, schema_editor):
    Location = apps.get_model('scheduler', 'Location')
    for location in Location.objects.all():
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
