# coding: utf-8
from django.contrib import admin
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from . import models
from organizations.admin import (
    MembershipFilteredAdmin,
    MembershipFieldListFilter
)


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

    get_volunteer_count.short_description = _(u'number of volunteers')
    get_volunteer_count.admin_order_field = 'volunteer_count'

    def get_volunteer_names(self, obj):
        def _format_username(user):
            full_name = user.get_full_name()
            username = u'{}<br><strong>{}</strong>'.format(user.username, user.email)
            if full_name:
                username = u'{} / {}'.format(full_name, username)
            return u'<li>{}</li>'.format(username)

        return u"<ul>{}</ul>".format(u"\n".join(_format_username(volunteer.user) for volunteer in
                          obj.helpers.all()))

    get_volunteer_names.short_description = _(u'volunteers')
    get_volunteer_names.allow_tags = True

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
