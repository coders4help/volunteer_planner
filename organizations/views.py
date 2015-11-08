# coding=utf-8

import itertools
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.template.defaultfilters import date
from django.utils.safestring import mark_safe
from django.views.generic import DetailView
from django_ajax.decorators import ajax
from accounts.models import UserAccount
from google_tools.templatetags.google_links import google_maps_directions
from news.models import NewsEntry
from organizations.admin import filter_queryset_by_membership
from scheduler.models import Shift
from .models import Organization, Facility, Membership, FacilityMembership


class OrganizationView(DetailView):
    template_name = 'organization.html'
    model = Organization

    def get_queryset(self):
        qs = super(OrganizationView, self).get_queryset()
        return qs.prefetch_related('facilities')


class FacilityView(DetailView):
    template_name = 'facility.html'
    model = Facility
    queryset = Facility.objects.select_related('organization')

    def get_context_data(self, **kwargs):
        context = super(FacilityView, self).get_context_data(**kwargs)
        shifts = Shift.open_shifts.filter(facility=self.object)
        context['object'] = self.object
        context['facility'] = get_facility_details(self.object, shifts)

        return context


class PendingApprovalsView(DetailView):
    """
    This view returns the pending member requests for approval by the shift
    planner for the already logged in
    shift planner of certain facilities.
    """

    model = Facility
    template_name = "approvals.html"
    queryset = Facility.objects.select_related('organization').prefetch_related(
        'memberships', 'memberships__user_account',
        'memberships__user_account__user')

    # def get_context_data(self, **kwargs):
    #     context = super(PendingApprovalsView, self).get_context_data(**kwargs)


@ajax
@staff_member_required
def managing_members_view(request):
    facility = Facility.objects.get(id=int(request.POST.get('facility_id')))
    user_account_id = UserAccount.objects.get(id=int(request.POST.get('user_account_id')))
    action = request.POST.get('action')
    membership = filter_queryset_by_membership(
        FacilityMembership.objects.get(facility=facility, user_account=user_account_id))
    if action == "remove":
        membership.delete()
    elif membership.status == membership.Status.PENDING:
        if action == "accept":
            membership.status = membership.Status.APPROVED
            membership.save()
        elif action == "reject":
            membership.status = membership.Status.REJECTED
            membership.save()
    return {'result': "successful"}


def get_facility_details(facility, shifts):
    address_line = facility.address_line if facility.address else None
    shifts_by_date = itertools.groupby(shifts, lambda s: s.starting_time.date())
    return {
        'name': facility.name,
        'url': facility.get_absolute_url(),
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
                           'facility_slug': facility.slug,
                           'year': shift_date.year,
                           'month': shift_date.month,
                           'day': shift_date.day,
                       })
                   } for shift_date, shifts_of_day in shifts_by_date],
        'organization': {
            'id': facility.organization.id,
            'name': facility.organization.name,
            'url': facility.organization.get_absolute_url(),
        }
    }


def _serialize_news(news_entries):
    return [dict(title=news_entry.title,
                 date=news_entry.creation_date,
                 text=news_entry.text) for news_entry in news_entries]
