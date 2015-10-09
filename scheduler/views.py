# coding: utf-8

import datetime
import logging
import json
import itertools

from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db.models import Count

from django.templatetags.l10n import localize

from django.utils.safestring import mark_safe

from django.views.generic import TemplateView, FormView, DetailView

from django.shortcuts import get_object_or_404

from django.utils.translation import ugettext_lazy as _

from accounts.models import UserAccount
from google_tools.templatetags.google_links import google_maps_directions
from scheduler.models import Location, Need, ShiftHelper
from notifications.models import Notification
from .forms import RegisterForNeedForm
from volunteer_planner.utils import LoginRequiredMixin

logger = logging.getLogger(__name__)


class HelpDesk(LoginRequiredMixin, TemplateView):
    """
    Location overview. First view that a volunteer gets redirected to when they log in.
    """
    template_name = "helpdesk.html"

    def get_context_data(self, **kwargs):
        context = super(HelpDesk, self).get_context_data(**kwargs)
        open_needs = Need.open_needs.select_related('location',
                                                    'location__place')
        open_needs = open_needs.order_by('location', 'starting_time')

        shifts_by_location = itertools.groupby(open_needs, lambda r: r.location)

        location_json = []
        used_places = set()

        for location, shifts_at_location in shifts_by_location:
            address_line = location.street + ", " + location.postal_code + " " + location.city
            shifts_by_date = itertools.groupby(shifts_at_location,
                                               lambda s: s.starting_time.date())
            used_places.add(location.place.area)
            location_json.append({
                'name': location.name,
                'address_line': address_line,
                'google_maps_link': google_maps_directions(address_line),
                'additional_info': mark_safe(location.additional_info),
                'area_slug': location.place.area.slug,
                'shifts': [{
                               'date_string': localize(shift_date),
                               'link': reverse('planner_by_location', kwargs={
                                   'pk': location.pk,
                                   'year': shift_date.year,
                                   'month': shift_date.month,
                                   'day': shift_date.day,
                               })
                           } for shift_date, shifts_of_day in shifts_by_date]
            })

        context['areas_json'] = json.dumps(
            [{'slug': area.slug, 'name': area.name} for area in
             sorted(used_places, key=lambda p: p.name)])
        context['location_json'] = json.dumps(location_json)
        context['notifications'] = Notification.objects.all().select_related(
            'location')
        return context


class PlannerView(LoginRequiredMixin, FormView):
    """
    View that gets shown to volunteers when they browse a specific day.
    It'll show all the available needs, and they can add and remove
    themselves from needs.
    """
    template_name = "helpdesk_single.html"
    form_class = RegisterForNeedForm

    def get_context_data(self, **kwargs):

        context = super(PlannerView, self).get_context_data(**kwargs)

        context['needs'] = Need.objects.filter(location__pk=self.kwargs['pk']) \
            .annotate(volunteer_count=Count('helpers')) \
            .filter(ending_time__year=self.kwargs['year'],
                    ending_time__month=self.kwargs['month'],
                    ending_time__day=self.kwargs['day']) \
            .order_by('topic', 'ending_time') \
            .select_related('topic', 'location') \
            .prefetch_related('helpers',
                              'helpers__user')

        context['location'] = get_object_or_404(Location, pk=self.kwargs['pk'])
        context['schedule_date'] = datetime.date(int(self.kwargs['year']),
                                                 int(self.kwargs['month']),
                                                 int(self.kwargs['day']))
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

        print(form.cleaned_data)

        if shift_to_join:

            conflicts = ShiftHelper.objects.conflicting(shift_to_join,
                                                        user_account=user_account)
            conflicted_needs = [shift_helper.need for shift_helper in conflicts]

            if conflicted_needs:
                error_message = _(
                    u'We can\'t add you to this shift because you\'ve already agreed to other shifts at the same time:')
                message_list = u'<ul>{}</ul>'.format('\n'.join(
                    [u'<li>{}</li>'.format(conflict) for conflict in
                     conflicted_needs]))
                messages.warning(self.request,
                                 mark_safe(u'{}<br/>{}'.format(error_message,
                                                               message_list)))
            else:
                shift_helper, created = ShiftHelper.objects.get_or_create(
                    user_account=user_account, need=shift_to_join)
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
                                        need=shift_to_leave).delete()
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
        return reverse('planner_by_location', kwargs=self.kwargs)


class GeographicHelpdeskView(DetailView):
    template_name = 'geographic_helpdesk.html'
    context_object_name = 'geographical_unit'

    def make_breadcrumps_dict(self, country, region=None, area=None,
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
        shifts = Need.open_needs.by_geography(place)
        shifts = shifts.select_related('topic',
                                       'location',
                                       'location__place',
                                       'location__place__area',
                                       'location__place__area__region',
                                       'location__place__area__region__country',
                                       )
        shifts = shifts.order_by('location__place__area__region__country',
                                 'location__place__area__region',
                                 'location__place__area',
                                 'location__place',
                                 'location',
                                 'ending_time',
                                 )
        context['shifts'] = shifts

        return context
