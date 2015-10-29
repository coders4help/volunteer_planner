# -*- coding: utf-8 -*-
from datetime import timedelta, datetime, time

from django.utils import formats
from django import forms
from django.conf.urls import url
from django.contrib import admin, messages
from django.core.urlresolvers import reverse
from django.db.models import Min, Count, Sum
from django.forms import DateInput, TimeInput
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.templatetags.l10n import localize
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _, ungettext_lazy

from . import models
from organizations.admin import (MembershipFilteredAdmin,
                                 MembershipFilteredTabularInline,
                                 MembershipFieldListFilter,
                                 filter_queryset_by_membership)
from scheduler import models as scheduler_models


class ShiftTemplateForm(forms.ModelForm):
    time_formats = formats.get_format('TIME_INPUT_FORMATS') + ('%H', '%H%M')

    class Meta:
        model = models.ShiftTemplate
        fields = '__all__'

    starting_time = forms.TimeField(label=_(u'starting time'),
                                    widget=TimeInput,
                                    input_formats=time_formats)
    ending_time = forms.TimeField(label=_(u'ending time'),
                                  widget=TimeInput,
                                  input_formats=time_formats)


class ShiftTemplateInline(MembershipFilteredTabularInline):
    model = models.ShiftTemplate

    min_num = 0
    extra = 0
    facility_filter_fk = 'schedule_template__facility'
    template = 'admin/scheduletemplates/shifttemplate/shift_template_inline.html'
    form = ShiftTemplateForm


JQUERYUI_FORMAT_MAPPING = {
    '%Y': 'yy',
    '%y': 'y',
    '%m': 'mm',
    '%b': 'M',
    '%d': 'dd',
    '%B': 'MM',
}


def translate_date_format(format_string, mappings=JQUERYUI_FORMAT_MAPPING):
    for k, v in mappings.iteritems():
        format_string = format_string.replace(k, v)
    return format_string


class ApplyTemplateForm(forms.Form):
    """
    Form that lets one select a date.

    TODO: Also select shifts via the form instead of inspecting raw POST data.
          https://docs.djangoproject.com/en/1.8/ref/forms/fields/#modelmultiplechoicefield
    """

    apply_for_date = forms.DateField(widget=DateInput)

    def __init__(self, *args, **kwargs):
        super(ApplyTemplateForm, self).__init__(*args, **kwargs)
        self.js_date_format = translate_date_format(
            formats.get_format_lazy('DATE_INPUT_FORMATS')[0])

    class Media:
        css = {
            'all': (
                'jquery/css/jquery-ui.min.css',
            )
        }
        js = (
            'jquery/js/jquery.min.js',
            'jquery/js/jquery-ui.min.js',
        )


@admin.register(models.ScheduleTemplate)
class ScheduleTemplateAdmin(MembershipFilteredAdmin):
    inlines = [ShiftTemplateInline]
    list_display = (
        'name',
        'facility',
        'get_slot_count',
        'get_shift_template_count',
        'get_earliest_starting_time',
        'get_latest_ending_time')
    list_filter = (
        ('facility', MembershipFieldListFilter),
    )
    search_fields = ('name',)
    list_select_related = True

    def response_change(self, request, obj):
        if "_save_and_apply" in request.POST:
            return redirect('admin:apply_schedule_template', obj._get_pk_val())
        return super(ScheduleTemplateAdmin, self).response_change(request, obj)

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
        context["opts"] = self.model._meta
        # Needed for admin template breadcrumbs

        # Phase 1
        if request.method == 'GET':
            # Empty form, prepopulated with tomorrow's date
            form = ApplyTemplateForm(
                initial={'apply_for_date': timezone.now().date() + timedelta(
                    days=1)})
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
            if not form.is_valid():
                # Shouldn't happen, but let's make sure we don't proceed with
                # applying shifts.
                raise ValueError("Invalid date format {}".format(form.errors))

            apply_date = form.cleaned_data['apply_for_date']

            # Get selected shifts.
            # TODO: This should be done with a ModelMultipleChoiceField on the form.
            id_list = request.POST.getlist('selected_shift_templates', [])

            selected_shift_templates = shift_templates.filter(id__in=id_list)

            # Phase 2: display a preview of whole day
            if request.POST.get('preview'):
                existing_shifts = scheduler_models.Shift.objects.filter(
                    facility=schedule_template.facility)
                existing_shifts = existing_shifts.on_shiftdate(apply_date)
                existing_shifts = existing_shifts.select_related('task',
                                                                 'workplace')
                existing_shifts = list(existing_shifts.annotate(
                    volunteer_count=Count('helpers')))

                if len(existing_shifts):
                    messages.warning(request, ungettext_lazy(
                        u'A shift already exists at {date}',
                        u'{num_shifts} shifts already exists at {date}',
                        len(id_list)).format(
                        num_shifts=len(existing_shifts),
                        date=localize(apply_date)))

                    combined_shifts = list(
                        selected_shift_templates) + existing_shifts

                    # returns (task, workplace, start_time and is_template)
                    # to make combined list sortable
                    def __shift_key(shift):
                        is_template = isinstance(shift, models.ShiftTemplate)
                        task = shift.task.id if shift.task else 0
                        workplace = shift.workplace.id if shift.workplace else 0
                        shift_start = shift.starting_time
                        if not isinstance(shift_start, time):
                            # can't compare starting_time of shift (datetime)
                            # and shift templates (time) directly
                            shift_start = shift_start.time()
                        return task, workplace, shift_start, is_template

                    combined_shifts = sorted(combined_shifts, key=__shift_key)
                else:
                    combined_shifts = selected_shift_templates

                context.update({
                    "schedule_template": schedule_template,
                    "selected_date": apply_date,
                    "selected_shifts": selected_shift_templates,
                    "existing_shifts": existing_shifts,
                    "combined_shifts": combined_shifts,
                    "apply_form": form,
                    # Needed because we need to POST the data again
                })

                return TemplateResponse(
                    request,
                    "admin/scheduletemplates/apply_template_confirm.html",
                    context)

            # Phase 3: Create shifts
            elif request.POST.get('confirm') or request.POST.get('confirm_and_repeat'):
                for template in selected_shift_templates:
                    starting_time = datetime.combine(apply_date,
                                                     template.starting_time)
                    scheduler_models.Shift.objects.create(
                        facility=template.schedule_template.facility,
                        starting_time=starting_time,
                        ending_time=starting_time + template.duration,
                        task=template.task,
                        workplace=template.workplace,
                        slots=template.slots)

                messages.success(request, ungettext_lazy(
                    u'{num_shifts} shift was added to {date}',
                    u'{num_shifts} shifts were added to {date}',
                    len(id_list)).format(
                    num_shifts=len(id_list),
                    date=localize(apply_date)))
                if request.POST.get('confirm'):
                    return redirect(
                        'admin:scheduletemplates_scheduletemplate_change', pk)
                else:
                    return redirect('admin:apply_schedule_template', pk)
            else:
                messages.error(request, _(
                    u'Something didn\'t work. Sorry about that.').format(
                    len(id_list),
                    localize(apply_date)))
                if request.POST.get('confirm'):
                    return redirect(
                        'admin:scheduletemplates_scheduletemplate_change', pk)
                else:
                    return redirect('admin:apply_schedule_template', pk)

    def get_urls(self):
        urls = super(ScheduleTemplateAdmin, self).get_urls()
        custom_urls = [
            url(r'^(?P<pk>.+)/apply/$',
                self.admin_site.admin_view(self.apply_schedule_template),
                name='apply_schedule_template'),
        ]
        return custom_urls + urls

    def get_queryset(self, request):
        qs = super(ScheduleTemplateAdmin, self).get_queryset(request)

        qs = qs.prefetch_related('shift_templates',
                                 'shift_templates__workplace',
                                 'shift_templates__task')
        qs = qs.annotate(shift_template_count=Count('shift_templates'),
                         min_start=Min('shift_templates__starting_time'),
                         slot_count=Sum('shift_templates__slots'))
        qs.order_by('facility', 'min_start')
        return qs

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
        except models.ShiftTemplate.DoesNotExist:
            pass
        return None

    get_latest_ending_time.short_description = _('to')


@admin.register(models.ShiftTemplate)
class ShiftTemplateAdmin(MembershipFilteredAdmin):
    form = ShiftTemplateForm
    list_display = (
        'get_edit_link',
        'schedule_template',
        'slots',
        'task',
        'workplace',
        'starting_time',
        'ending_time',
        'days',
    )
    list_filter = (
        ('schedule_template__facility', MembershipFieldListFilter),
        ('schedule_template', MembershipFieldListFilter),
        ('task', MembershipFieldListFilter),
        ('workplace', MembershipFieldListFilter),
    )
    search_fields = (
        'schedule_template__name',
        'task__name',
        'workplace__name',
        'schedule_template__facility__name',
        'schedule_template__facility__organization__name',
    )
    facility_filter_fk = 'schedule_template__facility'

    def get_field_queryset(self, db, db_field, request):
        qs = super(ShiftTemplateAdmin, self).get_field_queryset(
            db, db_field, request)
        if db_field.rel.to == models.ScheduleTemplate:
            qs = qs or db_field.rel.to.objects.all()
            qs = filter_queryset_by_membership(qs, request.user)
        return qs
