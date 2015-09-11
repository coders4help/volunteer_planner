import json
import datetime

from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models.aggregates import Sum
from django.http.response import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt

from .models import Location, Need, Topics, scheduledRegPro
from notifications.models import Notification
from registration.models import RegistrationProfile

class LoginRequiredMixin(object):

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class HomeView(TemplateView):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('helpdesk'))
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):

        if 'locations' not in kwargs:
            kwargs['locations'] = Location.objects.all()

        if 'notifications' not in kwargs:
            kwargs['notifications'] = Notification.objects.all()

        if 'statistics' not in kwargs:
            kwargs['statistics'] = Location.objects.all()

        return kwargs


@login_required
def helpdesk(request):
    response = {}
    response['locations'] = Location.objects.all()
    response['notifications'] = Notification.objects.all()
    if request.user.has_perm('scheduler.can_checkin'):
        response['can_checkin'] = True
        print 'hello'
    else:
        response['can_checkin'] = False
    return render(request, 'helpdesk.html', response)



class ProfileView(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = "profile_edit.html"
    success_url = reverse_lazy('profile_edit')

    def get_object(self, queryset=None):
        """
        Returns the object the view is displaying.

        By default this requires `self.queryset` and a `pk` or `slug` argument
        in the URLconf, but subclasses can override this to return any object.
        """
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()

        # Next, try looking up by primary key.
        pk = self.request.user.pk
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj


class PlannerView(LoginRequiredMixin, TemplateView):
    template_name = "helpdesk_single.html"

    def get_context_data(self, **kwargs):
        if 'needs' not in kwargs:
            kwargs['needs'] = Need.objects.filter(location__pk=self.kwargs['pk'])\
                .filter(time_period_to__date_time__year=self.kwargs['year'],
                        time_period_to__date_time__month=self.kwargs['month'],
                        time_period_to__date_time__day=self.kwargs['day'])\
                .order_by('topic', 'time_period_to__date_time')
        return kwargs


@login_required
def register_for_need(request):
    if request.method == "POST" and request.is_ajax:
        need_id = int(request.POST['id_need'])
        registration_profile = RegistrationProfile.objects.get(user=request.user.pk)
        need = Need.objects.get(id=need_id)
        scheduled_reg_profile = scheduledRegPro(
            registration_profile = registration_profile,
            need = need
        )
        scheduled_reg_profile.save()

        return HttpResponse(json.dumps({"data": "ok"}), content_type="application/json")
    else:
        pass


@login_required
def de_register_for_need(request):
    if request.method == "POST" and request.is_ajax:
        need_id = int(request.POST['id_need'])
        registration_profile = RegistrationProfile.objects.get(user=request.user.pk)
        need = Need.objects.get(id=need_id)
        scheduled_reg_profile = scheduledRegPro.objects.get(
            registration_profile = registration_profile,
            need = need
        )
        scheduled_reg_profile.delete()

        return HttpResponse(json.dumps({"data": "ok"}), content_type="application/json")
    else:
        pass


@login_required(login_url='/auth/login/')
@permission_required('location.can_view')
def volunteer_list(request, **kwargs):
    """
    Show list of volunteers for current shift
    """
    today = datetime.date.today()
    loc = get_object_or_404(Location, id=kwargs.get('loc_pk'))
    needs = Need.objects.filter(location=loc, time_period_to__date_time__contains=today)
    data = list(RegistrationProfile.objects.filter(needs__in=needs).distinct().values_list('user__email', flat=True))
    # add param ?type=json in url to get JSON data
    if request.GET.get('type') == 'json':
        return JsonResponse(data, safe=False)
    return render(request, 'volunteer_list.html', {'data': json.dumps(data), 'location': loc, 'today': today})

@login_required(login_url='/auth/login/')
@permission_required('scheduler.can_checkin')
def volunteer_checkin_list(request, **kwargs):
    """
    Show checkin list of volunteers for current shift
    """
    today = datetime.date.today()
    loc = get_object_or_404(Location, id=kwargs.get('loc_pk'))
    needs = Need.objects.filter(location=loc, time_period_to__date_time__contains=today)

    shifts = []

    for need in needs:
        shift = {
            'shift': need,
            'volunteers': [],
        }

        for srp in scheduledRegPro.objects.filter(need=need):
            shift['volunteers'].append(srp)

        shifts.append(shift)

    return render(request, 'volunteer_checkin_list.html', {'shifts': shifts, 'location': loc, 'today': today})


@login_required(login_url='/auth/login/')
@permission_required('scheduler.can_checkin')
@csrf_exempt
def checkin_volunteer(request):
    shift_id = int(request.POST.get('shift'))
    regpro_id = int(request.POST.get('regpro'))
    srp = scheduledRegPro.objects.get(need_id=shift_id,registration_profile_id=regpro_id)
    srp.did_show_up = True
    srp.save()

    return JsonResponse({},status=200)
