# coding=utf-8

import itertools

from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import date
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.utils.safestring import mark_safe
from django.utils.decorators import method_decorator
from django.db import transaction

from organizations.admin import get_cached_memberships, filter_queryset_by_membership, is_manager
from organizations.models import Task
from scheduler.models import Shift
from scheduler.forms import TaskForm, ShiftForm, ShiftFormSet
from news.models import NewsEntry
from google_tools.templatetags.google_links import google_maps_directions
from .models import Organization, Facility
from volunteer_planner.utils import LoginRequiredMixin


class ShiftManagementView(LoginRequiredMixin, ListView):
    """
    View which shows a list of open shifts for the managers organization
    and provides creation/editing/deletion actions.
    """
    template_name = "organizations/shift_manage.html"

    def get_queryset(self):
        """
        Get all shifts scheduled in future for the organization of the current user
        """
        open_shifts = Shift.open_shifts.all()
        open_shifts = filter_queryset_by_membership(open_shifts, self.request.user)

        return open_shifts

class ShiftViewMembershipsRequiredMixin(LoginRequiredMixin):
    """
    it checks whether current user is allowed to access the shift.
    """
    def get_object(self, queryset=None):
        shift = super(ShiftViewMembershipsRequiredMixin, self).get_object()

        current_user = self.request.user
        shift_facility = shift.facility
        shift_organization = shift.facility.organization

        if (is_manager(current_user, shift_organization.id, shift_facility.id)
            or current_user.is_superuser):
            return shift
        else:
            raise Http404

class ShiftCreateView(ShiftViewMembershipsRequiredMixin, CreateView):
    """
    A create view for essentially shift creation from Task and Shift formset.
    See also ShiftUpdateView
    """
    template_name = 'organizations/shift_form.html'
    model = Task
    form_class = TaskForm
    formset_class = ShiftFormSet
    success_url = '/shifts/'

    @method_decorator(permission_required('organizations.add_task'))
    @method_decorator(permission_required('scheduler.add_shift'))
    def dispatch(self, *args, **kwargs):
        return super(ShiftCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        """
        if task form is valid, try to save it along with shifts entered.
        """
        self.object = form.save()

        formset = self.get_formset()
        if not formset.is_valid():
            return super(ShiftCreateView, self).form_invalid(form)
        formset.instance = self.object
        for shift_form in formset:
            shift = shift_form.save(commit=False)
            shift.facility = formset.instance.facility
        formset.save()

        return super(ShiftCreateView, self).form_valid(form)

    def get_formset(self):
        if self.request.method == 'POST':
            return self.formset_class(self.request.POST)
        else:
            return self.formset_class()

    def get_context_data(self, **kwargs):
        data = super(ShiftCreateView, self).get_context_data(**kwargs)
        data.update({'task_form': self.get_form(),
                     'shift_formset': self.get_formset(),
                     'title': 'Create new shift',
                     'submit_btn_text': 'Create'})
        return data

class ShiftUpdateView(ShiftViewMembershipsRequiredMixin, UpdateView):
    """
    An update view for editing shift

    Unlike ShiftCreateView, this class doesn't actually use a formset, because
    this view is specificially for editing a certain shift by design.
    """
    template_name = 'organizations/shift_form.html'
    model = Shift
    form_class = ShiftForm
    success_url = '/shifts/'

    @method_decorator(permission_required('organizations.change_task'))
    @method_decorator(permission_required('scheduler.change_shift'))
    def dispatch(self, *args, **kwargs):
        return super(ShiftUpdateView, self).dispatch(*args, **kwargs)

    def get_readonly_taskform(self):
        task_form = TaskForm(instance=self.object.task)
        for boundfield in task_form:
            boundfield.field.widget.attrs['readonly'] = True
        return task_form

    def get_context_data(self, **kwargs):
        data = super(ShiftUpdateView, self).get_context_data(**kwargs)
        data.update({'task_form': self.get_readonly_taskform(),
                     'shift_formset': [self.get_form()],
                     'title': 'Edit shift',
                     'submit_btn_text': 'Save'})
        return data

class ShiftDeleteView(ShiftViewMembershipsRequiredMixin, DeleteView):
    """
    View for the deletion confirmation for a shift.
    """
    model = Shift
    template_name = "organizations/shift_confirm_delete.html"

    @method_decorator(permission_required('organizations.delete_task'))
    @method_decorator(permission_required('scheduler.delete_shift'))
    def dispatch(self, *args, **kwargs):
        return super(ShiftDeleteView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse("shift_management")


class OrganizationView(DetailView):
    template_name = 'organization.html'
    model = Organization

    def get_queryset(self):
        qs = super(OrganizationView, self).get_queryset()
        return qs.prefetch_related('facilities')


class FacilityView(DetailView):
    template_name = 'facility.html'
    model = Facility

    def get_context_data(self, **kwargs):
        context = super(FacilityView, self).get_context_data(**kwargs)
        shifts = Shift.open_shifts.filter(facility=self.object)
        context['facility'] = get_facility_details(self.object, shifts)
        return context


def get_facility_details(facility, shifts):
    address_line = facility.address_line if facility.address else None
    shifts_by_date = itertools.groupby(shifts, lambda s: s.starting_time.date())
    return {
        'name': facility.name,
        'news': _serialize_news(NewsEntry.objects.filter(facility=facility)),
        'address_line': address_line,
        'contact_info': facility.contact_info,
        'google_maps_link': google_maps_directions(
            address_line) if address_line else None,
        'description': mark_safe(facility.description),
        'area_slug': facility.place.area.slug,
        'shifts': [{
                       'date_string': date(shift_date),
                       'link': reverse('planner_by_facility', kwargs={
                           'pk': facility.pk,
                           'year': shift_date.year,
                           'month': shift_date.month,
                           'day': shift_date.day,
                       })
                   } for shift_date, shifts_of_day in shifts_by_date],
        'organization': {'id': facility.organization.id,
                         'name': facility.organization.name}
    }


def _serialize_news(news_entries):
    return [dict(title=news_entry.title,
                 date=news_entry.creation_date,
                 text=news_entry.text) for news_entry in news_entries]
