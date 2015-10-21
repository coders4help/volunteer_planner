# coding: utf-8
from django.contrib import admin
from django.db.models import Count

from . import models
from organizations.admin import MembershipFilteredAdmin, \
    MembershipFieldListFilter


@admin.register(models.Shift)
class ShiftAdmin(MembershipFilteredAdmin):
    def get_queryset(self, request):
        qs = super(ShiftAdmin, self).get_queryset(request)
        qs = qs.annotate(volunteer_count=Count('helpers'))
        qs = qs.select_related('facility',
                               'task',
                               'workplace')
        qs = qs.prefetch_related('helpers',
                                 'helpers__user')
        return qs

    def get_volunteer_count(self, obj):
        return obj.volunteer_count

    def get_volunteer_names(self, obj):
        def _format_username(user):
            full_name = user.get_full_name()
            if full_name:
                return u'{} ("{}")'.format(full_name, user.username)
            return u'"{}"'.format(user.username)

        return u", ".join(_format_username(volunteer.user) for volunteer in
                          obj.helpers.all())

    list_display = (
        'task',
        'workplace',
        'facility',
        'starting_time',
        'ending_time',
        'slots',
        'get_volunteer_count',
        'get_volunteer_names'
    )

    search_fields = ('id', 'task__name',)
    list_filter = (
        ('facility', MembershipFieldListFilter),
        'starting_time',
        'ending_time'
    )


@admin.register(models.ShiftHelper)
class ShiftHelperAdmin(MembershipFilteredAdmin):
    list_display = (u'id', 'user_account', 'shift', 'joined_shift_at')
    list_filter = ('joined_shift_at',)
    raw_id_fields = ('user_account', 'shift')
