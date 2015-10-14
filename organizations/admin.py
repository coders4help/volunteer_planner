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
    list_filter = ('organization',)
    raw_id_fields = ('user_account',)


admin.site.register(OrganizationMembership, OrganizationMembershipAdmin)


class FacilityMembershipAdmin(admin.ModelAdmin):
    list_display = (
        'role',
        'user_account',
        'facility'
    )
    list_filter = ('facility',)
    raw_id_fields = ('user_account',)

admin.site.register(FacilityMembership, FacilityMembershipAdmin)


class WorkplaceAdmin(admin.ModelAdmin):
    list_display = (
        'facility',
        'name',
        'description'
    )
    list_filter = ('facility',)
    search_fields = ('name', )

    def get_queryset(self, request):
        qs = super(WorkplaceAdmin, self).get_queryset(request)
        qs = qs.select_related('facility')
        return qs

admin.site.register(Workplace, WorkplaceAdmin)


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description'
    )
    search_fields = ('name',)

    def get_queryset(self, request):
        qs = super(TaskAdmin, self).get_queryset(request)
        qs = qs.select_related('facility')
        return qs


admin.site.register(Task, TaskAdmin)
