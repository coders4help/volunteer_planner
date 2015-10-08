# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def migrate_locations(apps, schema_editor):
    Location = apps.get_model('scheduler', 'Location')
    Organization = apps.get_model('organizations', 'Organization')
    Facility = apps.get_model('organizations', 'Facility')

    def merged_address(location):
        return u"{}\n{}".format(location.city,
                                u'{} {}'.format(location.postal_code,
                                                location.city).strip())

    def make_org_from_location(location):
        org = Organization()
        org.id = location.id
        org.name = location.name
        org.short_description = ""
        org.description = location.additional_info
        org.address = "TBD"
        org.contact_info = "TBD"

        org.save()
        return org

    for location in Location.objects.all():

        org = make_org_from_location(location)
        facility = Facility()
        facility.id = location.id
        facility.organization = org
        facility.name = location.name
        facility.short_description = ""
        facility.description = location.additional_info
        facility.address = merged_address(location)
        facility.zip_code = location.postal_code
        facility.contact_info = "TBD"
        facility.place = location.place
        facility.latitude = location.latitude
        facility.longitude = location.longitude
        facility.show_on_map = facility.latitude and facility.longitude

        facility.save()


def skip(_, __):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('organizations', '0001_initial'),
        ('scheduler', '0026_auto_20151002_0150'),
    ]

    operations = [
        migrations.RunPython(migrate_locations, skip)
    ]
