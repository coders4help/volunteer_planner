# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Organization, Facility, OrganizationMembership, FacilityMembership


class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        u'id',
        'name',
        'slug',
        'short_description',
        'description',
        'contact_info',
        'address',
    )
    raw_id_fields = ('members',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ['name']}
admin.site.register(Organization, OrganizationAdmin)


class FacilityAdmin(admin.ModelAdmin):
    list_display = (
        u'id',
        'organization',
        'name',
        'slug',
        'short_description',
        'description',
        'contact_info',
        'place',
        'address',
        'zip_code',
        'show_on_map',
        'latitude',
        'longitude',
    )
    list_filter = ('organization', 'place', 'show_on_map')
    raw_id_fields = ('members',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ['name']}
admin.site.register(Facility, FacilityAdmin)


class OrganizationMembershipAdmin(admin.ModelAdmin):
    list_display = (u'id', 'role', 'user_account', 'organization')
    list_filter = ('user_account', 'organization')
admin.site.register(OrganizationMembership, OrganizationMembershipAdmin)


class FacilityMembershipAdmin(admin.ModelAdmin):
    list_display = (u'id', 'role', 'user_account', 'facility')
    list_filter = ('user_account', 'facility')
admin.site.register(FacilityMembership, FacilityMembershipAdmin)

