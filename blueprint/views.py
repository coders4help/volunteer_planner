# coding: utf-8

import json

from django.http.response import HttpResponse
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from dateutil.parser import parse

from organizations.models import Facility
from scheduler.models import Need
from .models import BluePrintCreator


class SuperuserRequiredMixin(object):
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(SuperuserRequiredMixin, self).dispatch(*args, **kwargs)


class ExecuteBluePrintView(SuperuserRequiredMixin, TemplateView):
    template_name = "blueprint_executor.html"

    def get_context_data(self, **kwargs):

        if 'facilities' not in kwargs:
            kwargs['facilities'] = Facility.objects.all()
        return kwargs


@user_passes_test(lambda u: u.is_superuser)
def generate_blueprint(request):
    if request.method == 'POST' and request.is_ajax():
        facilities = json.loads(request.POST.get('facilities'))
        for facility_id in facilities:
            facility = Facility.objects.get(pk=facility_id)
            blueprint = BluePrintCreator.objects.get(facility=facility)
            message = []
            for need in blueprint.needs.all():
                time_from = parse(
                    request.POST.get('date') + " " + need.from_time,
                    ignoretz=True, fuzzy=True)
                time_to = parse(request.POST.get('date') + " " + need.to_time,
                                ignoretz=True, fuzzy=True)

                # TODO: remove string casting dates here??
                if Need.objects.filter(topic=need.topic,
                                       facility=facility,
                                       starting_time=str(time_from),
                                       ending_time=str(time_to)).count() > 0:
                    message.append('Ist bereits vorhanden')
                else:
                    Need.objects.create(topic=need.topic, facility=facility,
                                        starting_time=time_from,
                                        ending_time=time_to, slots=need.slots)
                    message.append('Ist angelegt worden!')

            return HttpResponse(json.dumps({"data": message}),
                                content_type="application/json")
