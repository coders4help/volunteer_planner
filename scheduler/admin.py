# coding: utf-8

from django.contrib import admin
from django.db.models import Count

from places.models import Region, Country, Area, Place
from scheduler.models import Need, Topics, Location


# @admin.register(Organization)
# class OrganizationAdmin(admin.ModelAdmin):
#     list_display = ('name', )
#     search_fields = ('name', 'description')


class NeedAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return super(NeedAdmin, self).get_queryset(request) \
            .annotate(volunteer_count=Count('registrationprofile')) \
            .prefetch_related('registrationprofile_set',
                              'registrationprofile_set__user')

    def get_volunteer_count(self, obj):
        return obj.volunteer_count

    def get_volunteer_names(self, obj):
        def _format_username(user):
            full_name = user.get_full_name()
            if full_name:
                return u'{} ("{}")'.format(full_name, user.username)
            return u'"{}"'.format(user.username)

        return u", ".join(_format_username(volunteer.user) for volunteer in
                          obj.registrationprofile_set.all())

    list_display = (
        'id', 'topic', 'starting_time', 'ending_time', 'slots',
        'get_volunteer_count', 'get_volunteer_names'
    )

    search_fields = ('id', 'topic__title',)
    list_filter = ('location',)


admin.site.register(Need, NeedAdmin)


class TopicsAdmin(admin.ModelAdmin):
    list_display = ('title', 'id')
    search_fields = ('id',)


admin.site.register(Topics, TopicsAdmin)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return Location.objects.select_related('place',
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
        'street',
        'city',
        'postal_code',
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
    search_fields = ('name',)
