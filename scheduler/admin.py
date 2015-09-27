# coding: utf-8
import logging
from django.core.exceptions import ValidationError
from django.forms import HiddenInput
import mistune
from django import forms

from django.contrib import admin
from django.db.models import Count
from django_bootstrap_markdown.widgets import MarkdownInput

from scheduler.models import Need, Topics, Location

logger = logging.getLogger(__name__)


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
    search_fields = ('id', 'title')

    def get_form(self, request, obj=None, **kwargs):
        kwargs['form'] = TopicsForm
        return super(TopicsAdmin, self).get_form(request, obj, **kwargs)


class TopicsForm(forms.ModelForm):
    description = forms.CharField(widget=MarkdownInput, required=False)
    description_raw = forms.CharField(widget=HiddenInput, required=False)

    def __init__(self, *args, **kwargs):
        super(TopicsForm, self).__init__(*args, **kwargs)
        self.initial['description'] = self.instance.description_raw

    def clean(self):
        parent = super(TopicsForm, self)
        changed = parent.changed_data

        if 'description_raw' in changed:
            self.add_error(ValidationError('You''re not supposed to modify this field!!!'))

        if 'description' in changed:
            cleaned_data = parent.clean()
            desc_raw = cleaned_data.get('description')
            cleaned_data.update({'description_raw': desc_raw})
            changed.append('description_raw')
            cleaned_data.update({'description': (mistune.markdown(desc_raw, renderer=TopicRenderer()))})


class TopicRenderer(mistune.Renderer):
    def __init__(self, **kwargs):
        if 'escape' not in kwargs:
            kwargs.update({'escape': True})
        super(TopicRenderer, self).__init__(**kwargs)

    def link(self, link, title, text):
        result = super(TopicRenderer, self).link(link, title, text)
        if result:
            result = result.replace('<a ', '<a style="text-decoration: underline" target="_blank" ')
        return result


admin.site.register(Topics, TopicsAdmin)
admin.site.register(Location)
