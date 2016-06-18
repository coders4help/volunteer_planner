# coding=utf-8

import itertools

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from django.template.defaultfilters import date
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView
from django_ajax.decorators import ajax

from accounts.models import UserAccount
from osm_tools.templatetags.osm_links import osm_search
from news.models import NewsEntry
from organizations.admin import filter_queryset_by_membership
from scheduler.models import Shift
from .models import Organization, Facility, FacilityMembership


class OrganizationView(DetailView):
    ''' Class-based view to show details of an organization and related
        facilities.
    
    Inherits from django generic DetailView. Overrides get_queryset to get
        facilities which belong to organization via
        queryset.prefetch_related().
    
    '''
    template_name = 'organization.html'
    model = Organization

    def get_queryset(self):
        qs = super(OrganizationView, self).get_queryset()
        return qs.prefetch_related('facilities')


class FacilityView(DetailView):
    ''' Class-based view to show details of a facility plus news
        and open shifts for that facility.
    
    Inherits from django generic DetailView. Overrides
        get_context_data(self, **kwargs) to get open shifts for that facility.
        Calls get_facility_details(facility, shifts) to get details of
        that facility.
    '''
    template_name = 'facility.html'
    model = Facility
    queryset = Facility.objects.select_related('organization')

    def get_context_data(self, **kwargs):
        context = super(FacilityView, self).get_context_data(**kwargs)
        shifts = Shift.open_shifts.filter(facility=self.object)
        news = NewsEntry.objects.for_facilities([self.object])
        context['object'] = self.object
        context['facility'] = get_facility_details(self.object, shifts, news)  # FIXME

        return context


@ajax
@staff_member_required
def managing_members_view(request, **kwargs):
    try:
        facilities_managed_by_user = filter_queryset_by_membership(
            Facility.objects.all(),
            request.user,
            skip_superuser=False)

        facilities = facilities_managed_by_user.filter(
            organization__slug=kwargs['organization__slug'],
            slug=kwargs['slug']
        )

        facility = facilities.get()

        user_account_id = request.POST.get('user_account_id')

        action = request.POST.get('action')

        membership = FacilityMembership.objects.get(facility=facility,
                                                    user_account__id=user_account_id)

        if action == "remove":
            membership.delete()
        if action == "reject":
            membership.status = membership.Status.REJECTED
            membership.save()
        elif membership.status == membership.Status.PENDING:
            if action == "accept":
                membership.status = membership.Status.APPROVED
                membership.save()
                send_membership_approved_notification(membership,
                                                      approved_by=request.user)

    except Exception:
        if settings.DEBUG:
            raise
        return HttpResponseForbidden()
    return {'result': "sucess"}


class ManageFacilityMembersView(DetailView):
    """
    This view returns the pending member requests for approval by the shift
    planner for the already logged in
    shift planner of certain facilities.
    """

    model = Facility
    template_name = "manage_members.html"

    def get_queryset(self):
        qs = super(ManageFacilityMembersView, self).get_queryset()
        qs = qs.select_related('organization')
        qs = qs.prefetch_related(
            'memberships',
            'memberships__user_account',
            'memberships__user_account__user')
        return filter_queryset_by_membership(qs,
                                             self.request.user,
                                             skip_superuser=False)


def send_membership_approved_notification(membership, approved_by):

    try:
        template = get_template('emails/membership_approved.txt')
        context = {
            "username": membership.user_account.user.username,
            "facility_name": membership.facility.name,
        }
        message = template.render(context)
        subject = _(u'volunteer-planner.org: Membership approved')

        from_email = settings.DEFAULT_FROM_EMAIL
        reply_to = approved_by.email
        to = membership.user_account.user.email

        addresses = (to,)

        mail = EmailMessage(subject=subject,
                            body=message,
                            to=addresses,
                            from_email=from_email,
                            reply_to=reply_to)
        mail.send()
    except:
        raise


def get_facility_details(facility, shifts, news_entries):
    address_line = facility.address_line if facility.address else None
    shifts_by_date = itertools.groupby(shifts, lambda s: s.starting_time.date())
    return {
        'name': facility.name,
        'url': facility.get_absolute_url(),
        'news': _serialize_news(news_entries.filter_by_facility(facility)),
        'address_line': address_line,
        'contact_info': facility.contact_info,
        'osm_link': osm_search(address_line) if address_line else None,
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
