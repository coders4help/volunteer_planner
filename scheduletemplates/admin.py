# -*- coding: utf-8 -*-
from django.conf.urls import url

from django.contrib import admin
from django.db.models import Min, Count, Sum
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _

from .models import ScheduleTemplate, ShiftTemplate


class ShiftTemplateInline(admin.TabularInline):
    model = ShiftTemplate
    min_num = 0
    extra = 0

    def get_field_queryset(self, db, db_field, request):

        qs = super(ShiftTemplateInline, self).get_field_queryset(db,
                                                                 db_field,
                                                                 request)
        if db_field.name in ('task', 'workplace', 'schedule_template'):
            qs = (qs or db_field.rel.to.objects.all()).select_related(
                'facility')

        return qs


class ScheduleTemplateAdmin(admin.ModelAdmin):
    inlines = [
        ShiftTemplateInline
    ]

    def apply_schedule_template(self, request, pk):
        schedule_template = get_object_or_404(self.model, pk=pk)
        context = dict(self.admin_site.each_context(request))
        context.update({
            "opts": self.model._meta,
            "schedule_template": schedule_template,
            "shift_templates": ShiftTemplate.objects.filter(schedule_template=schedule_template)
        })

        return TemplateResponse(request,
                                "admin/scheduletemplates/apply_template.html",
                                context)

    def get_urls(self):
        urls = super(ScheduleTemplateAdmin, self).get_urls()
        custom_urls = [
            url(r'^(?P<pk>.+)/apply/$',
                self.admin_site.admin_view(self.apply_schedule_template),
                name='apply_schedule_template'),
        ]
        return custom_urls + urls

    def get_slot_count(self, obj):
        return obj.slot_count

    get_slot_count.short_description = _('slots')
    get_slot_count.admin_order_field = 'slot_count'

    def get_shift_template_count(self, obj):
        return obj.shift_template_count

    get_shift_template_count.short_description = _('shifts')
    get_shift_template_count.admin_order_field = 'shift_template_count'

    def get_earliest_starting_time(self, obj):
        return obj.min_start

    get_earliest_starting_time.short_description = _('from')
    get_earliest_starting_time.admin_order_field = 'min_start'

    def get_latest_ending_time(self, obj):
        try:
            latest_shift = obj.shift_templates.order_by('-days',
                                                        '-ending_time')[
                           0:1].get()
            return latest_shift.localized_display_ending_time
        except ShiftTemplate.DoesNotExist:
            pass
        return None

    get_latest_ending_time.short_description = _('to')

    def get_queryset(self, request):
        qs = super(ScheduleTemplateAdmin, self).get_queryset(request)
        qs = qs.select_related('facility')
        qs = qs.prefetch_related('shift_templates',
                                 'shift_templates__workplace',
                                 'shift_templates__task')
        qs = qs.annotate(shift_template_count=Count('shift_templates'),
                         min_start=Min('shift_templates__starting_time'),
                         slot_count=Sum('shift_templates__slots'))
        qs.order_by('facility', 'min_start')
        return qs

    list_display = (
        'facility',
        'name',
        'get_slot_count',
        'get_shift_template_count',
        'get_earliest_starting_time',
        'get_latest_ending_time')
    list_filter = ('facility',)
    search_fields = ('name',)


admin.site.register(ScheduleTemplate, ScheduleTemplateAdmin)


class ShiftTemplateAdmin(admin.ModelAdmin):
    list_display = (
        u'id',
        'schedule_template',
        'slots',
        'task',
        'workplace',
        'starting_time',
        'ending_time',
        'days',

    )
    list_filter = ('schedule_template__facility', 'task', 'workplace')

    def get_field_queryset(self, db, db_field, request):

        qs = super(ShiftTemplateInline, self).get_field_queryset(db,
                                                                 db_field,
                                                                 request)
        if db_field.name in ('task', 'workplace', 'schedule_template'):
            qs = (qs or db_field.rel.to.objects.all()).select_related(
                'facility')
            if self.parent_model.facility:
                qs = qs.filter(facility=self.parent_model.facility)

        return qs


admin.site.register(ShiftTemplate, ShiftTemplateAdmin)
