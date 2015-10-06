# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import (Organization, Facility, OrganizationMembership,
                     FacilityMembership, Workplace, Task)


class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'short_description',
        'description',
        'contact_info',
        'address',
    )
    raw_id_fields = ('members',)
    search_fields = ('name',)


admin.site.register(Organization, OrganizationAdmin)


class FacilityAdmin(admin.ModelAdmin):
    list_display = (
        'organization',
        'name',
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
    search_fields = ('name', )


admin.site.register(Facility, FacilityAdmin)


class OrganizationMembershipAdmin(admin.ModelAdmin):
    list_display = (

        'user_account',
        'organization',
        'role',
    )
    list_filter = ('user_account', 'organization')


admin.site.register(OrganizationMembership, OrganizationMembershipAdmin)


class FacilityMembershipAdmin(admin.ModelAdmin):
    list_display = (
        'role',
        'user_account',
        'facility'
    )
    list_filter = ('user_account', 'facility')


admin.site.register(FacilityMembership, FacilityMembershipAdmin)


class WorkplaceAdmin(admin.ModelAdmin):
    list_display = (
        'facility',
        'name',
        'description'
    )
    list_filter = ('facility',)
    search_fields = ('name', )


admin.site.register(Workplace, WorkplaceAdmin)


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description'
    )
    search_fields = ('name',)


admin.site.register(Task, TaskAdmin)
