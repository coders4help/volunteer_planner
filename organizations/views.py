# coding=utf-8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy
from datetime import date

from volunteer_planner.utils import LoginRequiredMixin
from organizations.models import OrganizationMembership

from scheduler.models import Shift
from organizations.admin import filter_queryset_by_membership


@login_required()
def shift_management(request):
    current_user = request.user
    
    # Get all shifts scheduled in future for the organization of the current user
    open_shifts = Shift.open_shifts.all()
    open_shifts = filter_queryset_by_membership(open_shifts, current_user)

    context = {'shifts': open_shifts}
    return render(request, 'organizations/shift_manage.html', context)

@login_required()
def shift_new(request):
    context = {}

    return render(request, 'organizations/shift_new.html', context)

@login_required()
def shift_edit(request, shift_id):
    shift = Shift.objects.get(id=shift_id)

    context = {'shift': shift}

    return render(request, 'organizations/shift_edit.html', context)

@login_required()
def shift_delete(request, shift_id):
    context = {}

	# TODO: implement delete and redirect
    return render(request, 'organizations/shift_edit.html', context)

