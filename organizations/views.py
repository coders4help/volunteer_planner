# coding=utf-8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy

from volunteer_planner.utils import LoginRequiredMixin

from scheduler.models import Shift


@login_required()
def shift_management(request):
    
    # Get all shifts scheduled in future for the organization of the current user
    all_shifts = Shift.objects.all()
    # TODO apply filter for only future shifts
    
    context = {'shifts': all_shifts}
    
    return render(request, 'organizations/shift_manage.html', context)
