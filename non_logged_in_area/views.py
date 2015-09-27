import logging

from django.db.models.aggregates import Count
from django.http.response import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse

from notifications.models import Notification
from scheduler.models import Location
from places.models import Region

logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    template_name = "base_non_logged_in.html"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('helpdesk'))
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        context['regions'] = Region.objects.annotate(
            locations_count=Count('areas__places__locations')).exclude(
            locations_count=0).prefetch_related('areas', 'areas__region').all()
        context['locations'] = Location.objects.select_related('place',
                                                               'place__area',
                                                               'place__area__region').all()
        context['notifications'] = Notification.objects.all()
        return context
