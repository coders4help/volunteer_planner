# coding=utf-8
import logging

from django.db.models.aggregates import Count
from django.http.response import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse
from organizations.models import Facility
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
            facility_count=Count('areas__places__facilities')).exclude(
            facility_count=0).prefetch_related('areas', 'areas__region').all()
        context['facilities'] = Facility.objects.select_related('place',
                                                                'place__area',
                                                                'place__area__region').all()
        return context
