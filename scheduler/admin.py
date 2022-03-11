# coding: utf-8
from datetime import datetime
from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.utils.html import format_html, mark_safe
from django.utils.translation import gettext_lazy as _

from . import models
from organizations.admin import (
    MembershipFilteredAdmin,
    MembershipFieldListFilter
)


class ShiftAdminForm(forms.ModelForm):
    class Meta:
        model = models.Shift
        fields = ['facility', 'slots', 'task', 'workplace', 'starting_time', 'ending_time', 'members_only']

    def clean(self):
        """Validation of shift data, to prevent non-sense values to be entered"""
        # Check start and end times to be reasonable
        start = self.cleaned_data.get('starting_time')
        end = self.cleaned_data.get('ending_time')

        # No times, no joy
        if not start:
            self.add_error('starting_time', ValidationError(_('No start time given')))
        if not end:
            self.add_error('ending_time', ValidationError(_('No end time given')))

        # There is no known reason to modify shifts in the past
        if start:
            now = datetime.now()
            if start < now:
                self.add_error('starting_time', ValidationError(_('Start time in the past')))
            if end and not end > start:
                self.add_error('ending_time', ValidationError(_('End time not after start time')))

        return self.cleaned_data


@admin.register(models.Shift)
class ShiftAdmin(MembershipFilteredAdmin):
    form = ShiftAdminForm

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
            username = format_html(u'{}<br><strong>{}</strong>',
                                   user.username, user.email)
            if full_name:
                username = format_html(u'{} / {}', full_name, username)
            return format_html(u'<li>{}</li>', username)

        return format_html(u"<ul>{}</ul>", mark_safe(u"\n".join(
                _format_username(volunteer.user) for volunteer in
                obj.helpers.all())))

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
        'members_only',
        'starting_time',
        'ending_time'
    )


@admin.register(models.ShiftHelper)
class ShiftHelperAdmin(MembershipFilteredAdmin):
    list_display = (u'id', 'user_account', 'shift', 'joined_shift_at')
    list_filter = ('joined_shift_at',)
    raw_id_fields = ('user_account', 'shift')
