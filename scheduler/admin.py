# coding: utf-8
from django.contrib import admin
from django.db.models import Count

from . import models


@admin.register(models.Shift)
class ShiftAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return super(ShiftAdmin, self).get_queryset(request) \
            .annotate(volunteer_count=Count('helpers')) \
            .select_related('facility', 'task', 'workplace') \
            .prefetch_related('helpers',
                              'helpers__user')

    @staticmethod
    def get_volunteer_count(obj):
        return obj.volunteer_count

    @staticmethod
    def get_volunteer_names(obj):
        def _format_username(user):
            full_name = user.get_full_name()
            if full_name:
                return u'{} ("{}")'.format(full_name, user.username)
            return u'"{}"'.format(user.username)

        return u", ".join(_format_username(volunteer.user) for volunteer in
                          obj.helpers.all())

    list_display = (
        'id', 'task', 'workplace', 'facility', 'starting_time', 'ending_time',
        'slots',
        'get_volunteer_count', 'get_volunteer_names'
    )

    search_fields = ('id', 'task__name',)
    list_filter = ('facility',)


@admin.register(models.ShiftHelper)
class ShiftHelperAdmin(admin.ModelAdmin):
    list_display = (u'id', 'user_account', 'shift', 'joined_shift_at')
    list_filter = ('joined_shift_at',)
    raw_id_fields = ('user_account', 'shift')
