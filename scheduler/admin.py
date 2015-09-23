# coding: utf-8

from django.contrib import admin
from django.db.models import Count

from scheduler.models import Need, Topics, Location, Region, Area


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    search_fields = ('name', )


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'region')
    search_fields = ('name', 'region__name')
    list_filter = ('region', )


# @admin.register(Organization)
# class OrganizationAdmin(admin.ModelAdmin):
#     list_display = ('name', )
#     search_fields = ('name', 'description')


class NeedAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return super(NeedAdmin, self).get_queryset(request)\
            .annotate(volunteer_count=Count('registrationprofile'))\
            .prefetch_related('registrationprofile_set', 'registrationprofile_set__user')

    def get_volunteer_count(self, obj):
        return obj.volunteer_count

    def get_volunteer_names(self, obj):
        def _format_username(user):
            full_name = user.get_full_name()
            if full_name:
                return u'{} ("{}")'.format(full_name, user.username)
            return u'"{}"'.format(user.username)
        return u", ".join(_format_username(volunteer.user) for volunteer in obj.registrationprofile_set.all())

    list_display = (
        'id', 'topic', 'starting_time', 'ending_time', 'slots', 'get_volunteer_count', 'get_volunteer_names'
    )

    search_fields = ('id', 'topic__title',)
    list_filter = ('location',)


admin.site.register(Need, NeedAdmin)


class TopicsAdmin(admin.ModelAdmin):
    list_display = ('title', 'id')
    search_fields = ('id',)


admin.site.register(Topics, TopicsAdmin)
admin.site.register(Location)

