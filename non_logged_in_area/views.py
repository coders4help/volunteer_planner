import logging

from django.db import ProgrammingError, OperationalError
from django.db.models.aggregates import Count
from django.http.response import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse

from notifications.models import Notification
from scheduler.models import WorkDone
from places.models import Region, Place

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
        context['places'] = Place.objects.annotate(
            locations_count=Count('locations')).exclude(
            locations_count=0).select_related('area', 'area__region').all()
        for i in context['regions']:
            location = i
            pass
        # context['regions'] = Region.objects.all().prefetch_related('areas__places__locations')
        context['notifications'] = Notification.objects.all()
        try:
            work_done = WorkDone.objects.get(pk=1)
        except (WorkDone.DoesNotExist, ProgrammingError, OperationalError):
            # In case the unmanaged model isn't created correctly or a developer is e.g. using
            # SQLite instead of MySQL, we don't want to fail loud and hard. The work done is
            # auxiliary information and we just log a warning.
            logger.warning(
                u"Work done view couldn't be accessed. Is the SQL view created?")
            work_done = ""
        finally:
            context['working_hours'] = work_done
        return context
