# coding: utf-8

import json

from django.http.response import HttpResponse
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

from dateutil.parser import parse

from scheduler.models import Location, Need
from .models import BluePrintCreator


class SuperuserRequiredMixin(object):
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(SuperuserRequiredMixin, self).dispatch(*args, **kwargs)


class ExecuteBluePrintView(SuperuserRequiredMixin, TemplateView):
    template_name = "blueprint_executor.html"

    def get_context_data(self, **kwargs):

        if 'locations' not in kwargs:
            kwargs['locations'] = Location.objects.all()
        return kwargs


@user_passes_test(lambda u: u.is_superuser)
def generate_blueprint(request):
    if request.method == 'POST' and request.is_ajax():
        locations = json.loads(request.POST.get('locations'))
        for location_id in locations:
            location = Location.objects.get(pk=location_id)
            blueprint = BluePrintCreator.objects.get(location=location)
            message = []
            for need in blueprint.needs.all():
                time_from = parse(
                    request.POST.get('date') + " " + need.from_time,
                    ignoretz=True, fuzzy=True)
                time_to = parse(request.POST.get('date') + " " + need.to_time,
                                ignoretz=True, fuzzy=True)

                # TODO: remove string casting dates here??
                if Need.objects.filter(topic=need.topic,
                                       location=location,
                                       starting_time=str(time_from),
                                       ending_time=str(time_to)).count() > 0:
                    message.append('Ist bereits vorhanden')
                else:
                    Need.objects.create(topic=need.topic, location=location,
                                        starting_time=time_from,
                                        ending_time=time_to, slots=need.slots)
                    message.append('Ist angelegt worden!')

            return HttpResponse(json.dumps({"data": message}),
                                content_type="application/json")
