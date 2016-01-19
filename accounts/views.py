# coding: utf-8

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy

from datetime import date, timedelta

from volunteer_planner.utils import LoginRequiredMixin
from scheduler.models import ShiftHelper
from accounts.models import UserAccount



@login_required()
def user_account_detail(request):
    user = request.user
    return render(request, 'user_detail.html', {'user': user})


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    """
    Allows a user to update their profile.
    """
    fields = ['first_name', 'last_name', 'username']
    template_name = "user_account_edit.html"
    success_url = reverse_lazy('account_detail')

    def get_object(self, queryset=None):
        return self.request.user


@login_required()
def shift_list_active(request):
    """
    Delivers the list of shifts, a user has signed up for today and the future.

    :param request:
    :return:
    """
    user = request.user
    shifthelper = ShiftHelper.objects.filter(user_account=UserAccount.objects.get(user=user))
    shifts_today = shifthelper\
        .filter(shift__starting_time__day=date.today().day)\
        .order_by("shift__starting_time")
    shifts_tomorrow = shifthelper\
        .filter(shift__starting_time__day=date.today().day+1)\
        .order_by("shift__starting_time")
    shifts_day_after_tomorrow = shifthelper\
        .filter(shift__starting_time__day=date.today().day+2)\
        .order_by("shift__starting_time")
    shifts_further_future = shifthelper\
        .filter(shift__starting_time__gt=date.today() + timedelta(days=3))\
        .order_by("shift__starting_time")
        
    return render(request, 'shift_list.html', {'user': user,
                                               'shifts_today': shifts_today,
                                               'shifts_tomorrow': shifts_tomorrow,
                                               'shifts_day_after_tomorrow': shifts_day_after_tomorrow,
                                               'shifts_further_future': shifts_further_future})


@login_required()
def shift_list_done(request):
    """
    Delivers the list of shifts, a user has signed up in the past (starting from yesterday).

    :param request:
    :return:
    """
    user = request.user
    shifthelper = ShiftHelper.objects.filter(user_account=UserAccount.objects.get(user=user))
    shifts_past =shifthelper.filter(shift__ending_time__lt=date.today()).order_by("shift__starting_time")

    return render(request, 'shift_list_done.html', {'user': user,
                                                    'shifts_past': shifts_past})

