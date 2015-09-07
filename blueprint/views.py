import json
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from scheduler.models import Location, Need, Topics, TimePeriods
from dateutil.parser import parse
from .models import BluePrintCreator, NeedBluePrint


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
                time_from = parse(request.POST.get('date') + " " + need.from_time, ignoretz=True, fuzzy=True)
                time_to = parse(request.POST.get('date') + " " + need.to_time, ignoretz=True, fuzzy=True)
                if Need.objects.filter(topic=need.topic, location=location, time_period_from__date_time=str(time_from),
                                       time_period_to__date_time=str(time_to)).count() > 0:
                    message.append('Ist bereits vorhanden')
                else:
                    time_to_link = TimePeriods(date_time=time_to)
                    time_to_link.save()
                    time_from_link = TimePeriods(date_time=time_from)
                    time_from_link.save()
                    new_need = Need(
                        topic=need.topic,
                        location=location,
                        time_period_from=time_from_link,
                        time_period_to=time_to_link,
                        slots=need.slots
                    )
                    new_need.save()
                    message.append('Ist angelegt worden!')

            return HttpResponse(json.dumps({"data": message}), content_type="application/json")
