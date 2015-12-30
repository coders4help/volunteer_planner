# coding: utf-8
import random
import string

from django.contrib.auth import logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import models

from volunteer_planner.utils import LoginRequiredMixin


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
    """
    user = models.User.objects.get_by_natural_key(request.user.username)
    user.username = random_string()
    user.first_name = "Deleted"
    user.last_name = "User"
    request.user.email = random_string(24)+"@yy.yy"
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
