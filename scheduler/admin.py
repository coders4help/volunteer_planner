# coding: utf-8
from django.contrib import admin
from django.db.models import Count

from . import models


class NeedAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return super(NeedAdmin, self).get_queryset(request) \
            .annotate(volunteer_count=Count('helpers')) \
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
        'id', 'topic', 'starting_time', 'ending_time', 'slots',
        'get_volunteer_count', 'get_volunteer_names'
    )

    search_fields = ('id', 'topic__title',)
    list_filter = ('facility',)


admin.site.register(models.Need, NeedAdmin)


class ShiftHelperAdmin(admin.ModelAdmin):
    list_display = (u'id', 'user_account', 'need', 'joined_shift_at')
    list_filter = ('joined_shift_at',)
    raw_id_fields = ('user_account', 'need')


admin.site.register(models.ShiftHelper, ShiftHelperAdmin)


class TopicsAdmin(admin.ModelAdmin):
    list_display = (u'id', 'title', 'description')


admin.site.register(models.Topics, TopicsAdmin)
#
#
# class EnrolmentAdmin(admin.ModelAdmin):
#     list_display = (u'id', 'user_account', 'shift', 'joined_shift_at')
#     list_filter = ('user_account', 'shift', 'joined_shift_at')
#
#
# admin.site.register(Enrolment, EnrolmentAdmin)
#
#
# class RecurringEventAdmin(admin.ModelAdmin):
#     list_display = (
#         u'id',
#         'task',
#         'workplace',
#         'name',
#         'description',
#         'weekday',
#         'needed_volunteers',
#         'start_time',
#         'end_time',
#         'first_date',
#         'last_date',
#         'disabled',
#     )
#     list_filter = (
#         'task',
#         'workplace',
#         'first_date',
#         'last_date',
#         'disabled',
#     )
#     search_fields = ('name',)
#
#
# admin.site.register(RecurringEvent, RecurringEventAdmin)
#
#
# class ShiftAdmin(admin.ModelAdmin):
#     list_display = (
#         u'id',
#         'task',
#         'workplace',
#         'needed_volunteers',
#         'start_time',
#         'end_time',
#     )
#     list_filter = (
#         'task',
#         'workplace',
#         'start_time',
#         'end_time',
#     )
#     raw_id_fields = ('volunteers',)
#
#
# admin.site.register(Shift, ShiftAdmin)
