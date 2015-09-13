# coding: utf-8

from django.contrib import admin
from .models import *


class NeedAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'topic', 'time_period_from', 'time_period_to', 'slots', 'get_volunteer_total', 'get_volunteers'
    )

    search_fields = ('topic',)
    list_filter = ('location',)


admin.site.register(Need, NeedAdmin)


class TopicsAdmin(admin.ModelAdmin):
    list_display = ('title', 'id')
    search_fields = ('id',)


admin.site.register(Topics, TopicsAdmin)
admin.site.register(TimePeriods)
admin.site.register(Location)
