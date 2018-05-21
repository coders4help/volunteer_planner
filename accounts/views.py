# coding: utf-8
import random
import string

from django.contrib.auth import logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import models

from datetime import date, timedelta

from volunteer_planner.utils import LoginRequiredMixin
from scheduler.models import ShiftHelper
from accounts.models import UserAccount


@login_required()
def user_account_detail(request):
    """
    Just shows the user profile.

    :param request: http request
    :return: return value can be used in urls.py: url(r'^', user_account_detail, name="account_detail")
    """
    user = request.user
    return render(request, 'user_detail.html', {'user': user})


def random_string(length=30):
    """
    Creates a random string of uppercase and lowercase letters.

    :param length: (optional, default is 30) length of the string to be created
    """
    return u''.join(random.choice(string.ascii_letters) for x in range(length))


@login_required()
def account_delete_final(request):
    """
    This randomizes/anonymises the user profile. The account is set inactive.
    (regarding to django documentation setting inactive is preferred to deleting an account.)

    :param request: http request
    :return http response of user_detail_deleted-template that confirms deletion.
    """
    user = models.User.objects.get_by_natural_key(request.user.username)
    user.username = random_string()
    user.first_name = "Deleted"
    user.last_name = "User"
    user.email = random_string(24)+"@yy.yy"
    user.password = random_string(20)
    user.is_active = False
    user.save()

    logout(request)
    return render(request, 'user_detail_deleted.html')


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    """
    Allows a user to update his/her profile.
    """
    fields = ['first_name', 'last_name', 'username']
    template_name = "user_account_edit.html"
    success_url = reverse_lazy('account_detail')

    def get_object(self, queryset=None):
        return self.request.user


class AccountDeleteView(LoginRequiredMixin, UpdateView):
    """
    Allows a user to confirm he/she wants to delete the profile. This offers the last warning.
    """
    fields = ['first_name', 'last_name', 'username']
    template_name = "user_account_delete.html"

    def get_object(self, queryset=None):
        return self.request.user


@login_required()
def shift_list_active(request):
    """
    Delivers the list of shifts, a user has signed up for today and the future.

    :param request: http request
    :return: http response of rendered shift_list-template and user-shifts,
        ie.: user, shifts_today, shifts_tomorrow, shifts_day_after_tomorrow,
        shifts_further_future.
    """
    user = request.user
    shifthelper = ShiftHelper.objects.filter(user_account=UserAccount.objects.get(user=user))
    shifts_today = shifthelper \
        .filter(shift__starting_time__day=date.today().day,
                shift__starting_time__month=date.today().month,
                shift__starting_time__year=date.today().year) \
        .order_by("shift__starting_time")
    shifts_tomorrow = shifthelper \
        .filter(shift__starting_time__day=date.today().day + 1,
                shift__starting_time__month=date.today().month,
                shift__starting_time__year=date.today().year) \
        .order_by("shift__starting_time")
    shifts_day_after_tomorrow = shifthelper \
        .filter(shift__starting_time__day=date.today().day + 2,
                shift__starting_time__month=date.today().month,
                shift__starting_time__year=date.today().year) \
        .order_by("shift__starting_time")
    shifts_further_future = shifthelper \
        .filter(shift__starting_time__gt=date.today() + timedelta(days=3)) \
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

    :param request: http request
    :return: http response of rendered shift_list_done-template and user-date,
        ie.: user and shifts_past.
    """
    user = request.user
    shifthelper = ShiftHelper.objects.filter(user_account=UserAccount.objects.get(user=user))
    shifts_past = shifthelper.filter(shift__ending_time__lt=date.today()).order_by("shift__starting_time").reverse()

    return render(request, 'shift_list_done.html', {'user': user,
                                                    'shifts_past': shifts_past})


