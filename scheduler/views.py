# coding: utf-8

import json
import datetime

from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.views.generic import TemplateView, FormView

from django.contrib.auth.decorators import login_required, permission_required

from django.utils.translation import ugettext_lazy as _

from scheduler.models import Location, Need
from notifications.models import Notification
from registration.models import RegistrationProfile
from stats.models import ValueStore
from .forms import RegisterForNeedForm
from volunteer_planner.utils import LoginRequiredMixin


class HomeView(TemplateView):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('helpdesk'))
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['locations'] = Location.objects.all()
        context['notifications'] = Notification.objects.all()
        try:
            context['working_hours'] = ValueStore.objects.get(
                name="total-volunteer-hours")
        except ValueStore.DoesNotExist:
            context['working_hours'] = ""
        return context


class HelpDesk(LoginRequiredMixin, TemplateView):
    """
    Location overview. First view that a volunteer gets redirected to when they log in.
    """
    template_name = "helpdesk.html"

    def get_context_data(self, **kwargs):
        context = super(HelpDesk, self).get_context_data(**kwargs)
        locations = context['locations'] = Location.objects.all()
        the_dates = [{loc: loc.get_dates_of_needs()} for loc in locations]
        context['need_dates_by_location'] = the_dates
        context['notifications'] = Notification.objects.all()
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
            .annotate(volunteer_count=Count('registrationprofile')) \
            .filter(time_period_to__date_time__year=self.kwargs['year'],
                    time_period_to__date_time__month=self.kwargs['month'],
                    time_period_to__date_time__day=self.kwargs['day']) \
            .order_by('topic', 'time_period_to__date_time') \
            .select_related('topic', 'location', 'time_period_from',
                            'time_period_to') \
            .prefetch_related('registrationprofile_set',
                              'registrationprofile_set__user')
        return context

    def form_invalid(self, form):
        messages.warning(self.request, _(u'The submitted data was invalid.'))
        return super(PlannerView, self).form_invalid(form)

    def form_valid(self, form):
        reg_profile = self.request.user.registrationprofile
        need = form.cleaned_data['need']
        if form.cleaned_data['action'] == RegisterForNeedForm.ADD:
            conflicts = need.get_conflicting_needs(reg_profile.needs.all())
            if conflicts:
                conflicts_string = u", ".join(
                    u'{}'.format(conflict) for conflict in conflicts)
                messages.warning(self.request,
                                 _(
                                     u'We can\'t add you to this shift because you\'ve already agreed to other shifts at the same time: {conflicts}'.format(
                                         conflicts=
                                         conflicts_string)))
            else:
                messages.success(self.request, _(
                    u'You were successfully added to this shift.'))
                reg_profile.needs.add(need)
        elif form.cleaned_data['action'] == RegisterForNeedForm.REMOVE:
            reg_profile.needs.remove(need)
        reg_profile.save()
        return super(PlannerView, self).form_valid(form)

    def get_success_url(self):
        """
        Redirect to the same page.
        """
        return reverse('planner_by_location', kwargs=self.kwargs)


@login_required(login_url='/auth/login/')
@permission_required('location.can_view')
def volunteer_list(request, **kwargs):
    """
    Show list of volunteers for current shift
    """
    today = datetime.date.today()
    loc = get_object_or_404(Location, id=kwargs.get('loc_pk'))
    needs = Need.objects.filter(location=loc,
                                time_period_to__date_time__contains=today)
    data = list(RegistrationProfile.objects.filter(
        needs__in=needs).distinct().values_list('user__email', flat=True))
    # add param ?type=json in url to get JSON data
    if request.GET.get('type') == 'json':
        return JsonResponse(data, safe=False)
    return render(request, 'volunteer_list.html',
                  {'data': json.dumps(data), 'location': loc, 'today': today})
