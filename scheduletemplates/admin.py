# -*- coding: utf-8 -*-
from datetime import timedelta, datetime

from django import forms
from django.conf.urls import url
from django.contrib import admin, messages
from django.db.models import Min, Count, Sum
from django.forms.extras import SelectDateWidget
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.templatetags.l10n import localize
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .models import ScheduleTemplate, ShiftTemplate
from scheduler.models import Shift


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


class ApplyTemplateForm(forms.Form):
    """
    Form that lets one select a date. We mostly use it because it lets us use
    Django's decent enough date selector.

    TODO: Also select shifts via the form instead of inspecting raw POST data.
          https://docs.djangoproject.com/en/1.8/ref/forms/fields/#modelmultiplechoicefield
    """
    apply_for_date = forms.DateField(widget=SelectDateWidget)


class ScheduleTemplateAdmin(admin.ModelAdmin):
    inlines = [ShiftTemplateInline]

    def apply_schedule_template(self, request, pk):
        """
        Juicy function that lets one create a schedule template, and
        then apply the template on one date to create individual shifts.

        Has three phases:
        1. GET: Allow selecting date and shifts
        2. POST: Displays a preview of what will be done
        3. POST: Actually apply the template.
        """
        schedule_template = get_object_or_404(self.model, pk=pk)
        shift_templates = schedule_template.shift_templates.all()

        context = dict(self.admin_site.each_context(request))
        context["opts"] = self.model._meta  # Needed for admin template breadcrumbs

        # Phase 1
        if request.method == 'GET':
            # Empty form, prepopulated with tomorrow's date
            form = ApplyTemplateForm(
                initial={'apply_for_date': timezone.now().date() + timedelta(days=1)})
            context.update({
                "schedule_template": schedule_template,
                "shift_templates": shift_templates,
                "apply_form": form,
            })

            return TemplateResponse(
                request, "admin/scheduletemplates/apply_template.html", context)

        # Phase 2 and 3
        elif request.method == 'POST':
            # Verify the form data.
            form = ApplyTemplateForm(request.POST)
            if form.is_valid():
                apply_date = form.cleaned_data['apply_for_date']
            else:
                # Shouldn't happen, but let's make sure we don't proceed with
                # applying shifts.
                raise ValueError("Invalid date format")

            # Get selected shifts.
            # TODO: This should be done with a ModelMultipleChoiceField on the form.
            id_list = request.POST.getlist('selected_shift_templates', [])
            selected_shift_templates = shift_templates.filter(id__in=id_list)

            # Phase 2: display a preview
            if request.POST.get('apply'):
                context.update({
                    "schedule_template": schedule_template,
                    "selected_shifts": selected_shift_templates,
                    "selected_date": apply_date,
                    "apply_form": form,  # Needed because we need to POST the data again
                })
                return TemplateResponse(
                    request, "admin/scheduletemplates/apply_template_confirm.html", context)

            # Phase 3: Create shifts
            elif request.POST.get('confirm'):
                for template in selected_shift_templates:
                    starting_time = datetime.combine(apply_date, template.starting_time)
                    Shift.objects.create(
                        starting_time=starting_time,
                        ending_time=starting_time + template.duration,
                        task=template.task,
                        workplace=template.workplace,
                        slots=template.slots)

                messages.success(request, _(
                    u'{} shifts were added to {}').format(len(id_list), localize(apply_date)))

                return redirect('admin:scheduletemplates_scheduletemplate_change', pk)

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

    def get_queryset(self, request):
        qs = super(ShiftTemplateAdmin, self).get_queryset(request)
        return self.model.objects.select_related('schedule_template',
                                                 'schedule_template__facility',
                                                 'workplace',
                                                 'workplace__facility',
                                                 'task',
                                                 'task__facility'
                                                 )
        return qs


admin.site.register(ShiftTemplate, ShiftTemplateAdmin)
