# coding=utf-8

import itertools

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import date
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.utils.safestring import mark_safe
from django.db import transaction

from organizations.admin import get_cached_memberships, filter_queryset_by_membership
from organizations.models import Task
from scheduler.models import Shift
from scheduler.forms import TaskForm, ShiftForm
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
        current_user = self.request.user
        
        if (not current_user.has_perm('scheduler.delete_shift')):
            raise Http404
        
        open_shifts = Shift.open_shifts.all()
        open_shifts = filter_queryset_by_membership(open_shifts, current_user)

        return open_shifts


class ShiftViewSaveMixin(LoginRequiredMixin):
    """
    it helps ShiftViews to save Shift and Task models from single request.
    """
    def form_valid(self, form):
        data = self.get_context_data()
        task_form = data['task_form']

        if not task_form.is_valid():
            return super(object, self).form_invalid(form)

        with transaction.atomic():
            task = task_form.save()

            form.instance.task = task
            form.instance.facility = task.facility
            self.object = form.save()

        return super(ShiftViewSaveMixin, self).form_valid(form)


class ShiftCreateView(ShiftViewSaveMixin, CreateView):
    template_name = 'organizations/shift_form.html'
    model = Shift
    form_class = ShiftForm
    success_url = '/shifts/'

    def get_context_data(self, **kwargs):
        data = super(ShiftCreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            data['task_form'] = TaskForm(self.request.POST)
        else:
            data['task_form'] = TaskForm()
        return data


class ShiftUpdateView(ShiftViewSaveMixin, UpdateView):
    """
    TODO: access permission needs to be checked before data gets updated in DB.
    """

    slug_field = 'id'
    slug_url_kwarg = 'id'
    template_name = 'organizations/shift_form.html'
    model = Shift
    form_class = ShiftForm
    success_url = '/shifts/'

    def get_context_data(self, **kwargs):
        data = super(ShiftUpdateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            data['task_form'] = TaskForm(self.request.POST)
        else:
            form = self.get_form()
            data['task_form'] = TaskForm(instance=form.instance.task)
        return data


class ShiftDeleteView(DeleteView):
    """
    View for the deletion confirmation for a shift.
    """
    model = Shift
    template_name = "organizations/shift_confirm_delete.html"

    def get_object(self, queryset=None):
        """
        Make sure that current user is allowed to delete the shift
        """
        shift = super(ShiftDeleteView, self).get_object()
        current_user = self.request.user
        facility = shift.facility
        
        if (self.can_delete_shift(current_user, facility)):
            return shift
        else:
            raise Http404

    def get_success_url(self):
        return reverse("shift_management")
        
    def can_delete_shift(self, user, facility):
        """
        Check if user has the general deletion rights and belongs
        to the given facility.
        """
        if (not user.has_perm('scheduler.delete_shift')):
            return False
        user_facilities = get_cached_memberships(user)[1]
        for facility_id in user_facilities:
            if facility_id == facility.id:
                return True
        return False


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
