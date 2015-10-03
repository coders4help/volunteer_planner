# coding: utf-8

from django.contrib import admin

from .models import (Organization,
                     Facility,
                     OrganizationMembership,
                     FacilityMembership)
from places.models import Place, Area, Region, Country


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


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return FacilityAdmin.objects.select_related('place',
                                                    'place__area',
                                                    'place__area__region',
                                                    'place__area__region__country')

    def get_place_name(self, obj):
        return obj.place.name

    get_place_name.short_description = Place._meta.verbose_name
    get_place_name.admin_order_field = 'place'

    def get_area_name(self, obj):
        return obj.place.area.name

    get_area_name.short_description = Area._meta.verbose_name
    get_area_name.admin_order_field = 'place__area'

    def get_region_name(self, obj):
        return obj.place.area.region.name

    get_region_name.short_description = Region._meta.verbose_name
    get_region_name.admin_order_field = 'place__area__region'

    def get_country_name(self, obj):
        return obj.place.area.region.country.name

    get_country_name.short_description = Country._meta.verbose_name
    get_country_name.admin_order_field = 'place__area__region__country'

    list_display = (
        'name',
        'organization',
        'address',
        'get_place_name',
        'get_area_name',
        'get_region_name',
        'get_country_name',
    )
    list_filter = (
        # 'place',
        'place__area',
        'place__area__region',
        'place__area__region__country'
    )
    prepopulated_fields = {'slug': ['name']}
    search_fields = ('name', 'organization__name',)


class OrganizationMembershipAdmin(admin.ModelAdmin):
    list_display = (u'id', 'role', 'user_account', 'organization')
    list_filter = ('user_account', 'organization')


admin.site.register(OrganizationMembership, OrganizationMembershipAdmin)


class FacilityMembershipAdmin(admin.ModelAdmin):
    list_display = (u'id', 'role', 'user_account', 'facility')
    list_filter = ('user_account', 'facility')


admin.site.register(FacilityMembership, FacilityMembershipAdmin)
