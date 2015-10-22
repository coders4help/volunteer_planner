# coding: utf-8

from datetime import date, datetime
import logging
import json
import itertools
from time import mktime
from django.core.serializers.json import DjangoJSONEncoder

from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db.models import Count
from django.templatetags.l10n import localize
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView, FormView, DetailView
from django.shortcuts import get_object_or_404

from django.utils.translation import ugettext_lazy as _

from accounts.models import UserAccount
from organizations.models import Facility
from news.models import News
from scheduler.models import Shift
from google_tools.templatetags.google_links import google_maps_directions
from scheduler.models import ShiftHelper
from .forms import RegisterForShiftForm
from volunteer_planner.utils import LoginRequiredMixin

from restless.models import serialize
from restless.views import Endpoint

logger = logging.getLogger(__name__)

class GetLocationData(Endpoint):
    def get(self, request, pk):
        return serialize(Location.objects.get(pk=pk), include=[
            ('dates', lambda l: [{'year': v[0].year, 'month': v[0].month, 'day': v[0].day, 'date_str': v[1]} for v in l.get_days_with_needs()])
        ])

def get_open_shifts():
    shifts = Shift.open_shifts.all()
    shifts = shifts.select_related('facility',
                                   'facility__place',
                                   'facility__place__area',
                                   'facility__place__area__region',
                                   'facility__place__area__region__country',
                                   )

    shifts = shifts.order_by('facility__place__area__region__country',
                             'facility__place__area__region',
                             'facility__place__area',
                             'facility__place',
                             'facility',
                             'starting_time',
                             )
    return shifts


def getNewsFacility(facility):
    news_query = News.objects.filter(facility=facility)
    news = []
    if news_query:

        for item in news_query:
            news.append({
                'title':item.title,
                'date':item.creation_date,
                'text':item.text
            })
    return news


class HelpDesk(LoginRequiredMixin, TemplateView):
    """
    Facility overview. First view that a volunteer gets redirected to when they log in.
    """
    template_name = "helpdesk.html"

    def get_context_data(self, **kwargs):
        context = super(HelpDesk, self).get_context_data(**kwargs)
        open_shifts = get_open_shifts()

        shifts_by_facility = itertools.groupby(open_shifts,
                                               lambda s: s.facility)

        facility_list = []
        used_places = set()

        for facility, shifts_at_facility in shifts_by_facility:
            address_line = facility.address_line if facility.address else None
            shifts_by_date = itertools.groupby(shifts_at_facility,
                                               lambda s: s.starting_time.date())
            used_places.add(facility.place.area)
            facility_list.append({
                'name': facility.name,
                'news': getNewsFacility(facility),
                'address_line': address_line,
                'google_maps_link': google_maps_directions(
                    address_line) if address_line else None,
                'description': mark_safe(facility.description),
                'area_slug': facility.place.area.slug,
                'shifts': [{
                               'date_string': localize(shift_date),
                               'link': reverse('planner_by_facility', kwargs={
                                   'pk': facility.pk,
                                   'year': shift_date.year,
                                   'month': shift_date.month,
                                   'day': shift_date.day,
                               })
                           } for shift_date, shifts_of_day in shifts_by_date]
            })

        context['areas_json'] = json.dumps(
            [{'slug': area.slug, 'name': area.name} for area in
             sorted(used_places, key=lambda p: p.name)])
        context['facility_json'] = json.dumps(facility_list, cls=DjangoJSONEncoder)
        context['shifts'] = open_shifts
        return context


class GeographicHelpdeskView(DetailView):
    template_name = 'geographic_helpdesk.html'
    context_object_name = 'geographical_unit'

    @staticmethod
    def make_breadcrumps_dict(country, region=None, area=None,
                              place=None):

        result = dict(country=country, flattened=[country, ])

        for k, v in zip(('region', 'area', 'place'), (region, area, place)):
            if v:
                result[k] = v
                result['flattened'].append(v)

        return result

    def get_queryset(self):
        return super(GeographicHelpdeskView,
                     self).get_queryset().select_related(
            *self.model.get_select_related_list())

    def get_context_data(self, **kwargs):
        context = super(GeographicHelpdeskView, self).get_context_data(**kwargs)
        place = self.object
        context['breadcrumps'] = self.make_breadcrumps_dict(*place.breadcrumps)
        context['shifts'] = get_open_shifts().by_geography(place)
        return context


class PlannerView(LoginRequiredMixin, FormView):
    """
    View that gets shown to volunteers when they browse a specific day.
    It'll show all the available shifts, and they can add and remove
    themselves from shifts.
    """
    template_name = "helpdesk_single.html"
    form_class = RegisterForShiftForm

    def get_context_data(self, **kwargs):

        context = super(PlannerView, self).get_context_data(**kwargs)
        schedule_date = date(int(self.kwargs['year']),
                             int(self.kwargs['month']),
                             int(self.kwargs['day']))
        facility = get_object_or_404(Facility, pk=self.kwargs['pk'])

        shifts = Shift.objects.filter(facility=facility)
        shifts = shifts.on_shiftdate(schedule_date)
        shifts = shifts.annotate(volunteer_count=Count('helpers'))
        shifts = shifts.order_by('task', 'ending_time')
        shifts = shifts.select_related('task', 'workplace', 'facility')
        shifts = shifts.prefetch_related('helpers', 'helpers__user')

        context['shifts'] = shifts
        context['facility'] = facility
        context['schedule_date'] = schedule_date
        return context

    def form_invalid(self, form):
        messages.warning(self.request, _(u'The submitted data was invalid.'))
        return super(PlannerView, self).form_invalid(form)

    def form_valid(self, form):
        try:
            user_account = self.request.user.account
        except UserAccount.DoesNotExist:
            messages.warning(self.request, _(u'User account does not exist.'))
            return super(PlannerView, self).form_valid(form)

        shift_to_join = form.cleaned_data.get("join_shift")
        shift_to_leave = form.cleaned_data.get("leave_shift")

        if shift_to_join:

            conflicts = ShiftHelper.objects.conflicting(shift_to_join,
                                                        user_account=user_account)
            conflicted_shifts = [shift_helper.shift for shift_helper in
                                 conflicts]

            if conflicted_shifts:
                error_message = _(
                    u'We can\'t add you to this shift because you\'ve already agreed to other shifts at the same time:')
                message_list = u'<ul>{}</ul>'.format('\n'.join(
                    [u'<li>{}</li>'.format(conflict) for conflict in
                     conflicted_shifts]))
                messages.warning(self.request,
                                 mark_safe(u'{}<br/>{}'.format(error_message,
                                                               message_list)))
            else:
                shift_helper, created = ShiftHelper.objects.get_or_create(
                    user_account=user_account, shift=shift_to_join)
                if created:
                    messages.success(self.request, _(
                        u'You were successfully added to this shift.'))
                else:
                    messages.warning(self.request, _(
                        u'You already signed up for this shift at {date_time}.').format(
                        date_time=shift_helper.joined_shift_at))
        elif shift_to_leave:
            try:
                ShiftHelper.objects.get(user_account=user_account,
                                        shift=shift_to_leave).delete()
            except ShiftHelper.DoesNotExist:
                # just catch the exception,
                # user seems not to have signed up for this shift
                pass
            messages.success(self.request, _(
                u'You successfully left this shift.'))

        user_account.save()
        return super(PlannerView, self).form_valid(form)

    def get_success_url(self):
        """
        Redirect to the same page.
        """
        return reverse('planner_by_facility', kwargs=self.kwargs)
