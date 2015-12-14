# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def migrate_locations(apps, schema_editor):
    locationModel = apps.get_model('scheduler', 'Location')
    organizationModel = apps.get_model('organizations', 'Organization')
    facilityModel = apps.get_model('organizations', 'Facility')
    needModel = apps.get_model('scheduler', 'Need')

    def merged_address(location):
        return u"{}\n{}".format(location.street,
                                u'{} {}'.format(location.postal_code,
                                                location.city).strip())

    def make_org_from_location(location):
        org = organizationModel()
        org.id = location.id
        org.name = location.name
        org.short_description = ""
        org.description = location.additional_info
        org.address = "TBD"
        org.contact_info = "TBD"

        org.save()
        return org

    for location in locationModel.objects.all():

        org = make_org_from_location(location)
        facility = facilityModel()
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

    for need in needModel.objects.all():

        need.facility_id = need.location_id
        need.save()


def skip(_, __):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('organizations', '0001_initial'),
        ('scheduler', '0028_need_facility'),
    ]

    operations = [
        migrations.RunPython(migrate_locations, skip)
    ]
