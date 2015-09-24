# coding: utf-8

import datetime
import logging

from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db.models import Count
from django.views.generic import TemplateView, FormView

from django.utils.translation import ugettext_lazy as _

from django.shortcuts import get_object_or_404

from scheduler.models import Location, Need, WorkDone
from notifications.models import Notification
from registration.models import RegistrationProfile
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
        shifts = Need.objects.filter(ending_time__gt=datetime.datetime.now()) \
            .order_by('location').select_related('location')
        context['shifts'] = shifts
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
            .annotate(volunteer_count=Count('registrationprofile')) \
            .filter(ending_time__year=self.kwargs['year'],
                    ending_time__month=self.kwargs['month'],
                    ending_time__day=self.kwargs['day']) \
            .order_by('topic', 'ending_time') \
            .select_related('topic', 'location') \
            .prefetch_related('registrationprofile_set',
                              'registrationprofile_set__user')

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
            reg_profile = self.request.user.registrationprofile
        except RegistrationProfile.DoesNotExist:
            messages.warning(self.request, _(u'User profile does not exist.'))
            return super(PlannerView, self).form_valid(form)

        join_shift = form.cleaned_data.get("join_shift")
        leave_shift = form.cleaned_data.get("leave_shift")

        print(form.cleaned_data)

        if join_shift:
            conflicts = join_shift.get_conflicting_needs(
                reg_profile.needs.all())
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
                reg_profile.needs.add(join_shift)
        elif leave_shift:
            messages.success(self.request, _(
                u'You successfully left this shift.'))
            reg_profile.needs.remove(leave_shift)
        reg_profile.save()
        return super(PlannerView, self).form_valid(form)

    def get_success_url(self):
        """
        Redirect to the same page.
        """
        return reverse('planner_by_location', kwargs=self.kwargs)
