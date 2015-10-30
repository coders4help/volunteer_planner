# coding=utf-8
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView
from django.core.urlresolvers import reverse_lazy
from django.db import transaction

from datetime import date

from volunteer_planner.utils import LoginRequiredMixin
from organizations.models import OrganizationMembership, Task

from scheduler.forms  import TaskForm, ShiftForm
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

# ------------------------------------------------------------------------------
class ShiftViewSaveMixin(LoginRequiredMixin):
    """
    it helps ShiftViews to save Shift and Task models from single request.
    """
    def form_valid(self, form):
        data = self.get_context_data()
        task_form = data['task_form']

        if not task_form.is_valid():
            return super(object, self).form_invalid(form)

        with transaction.atomic():
            task = task_form.save()

            form.instance.task = task
            form.instance.facility = task.facility
            self.object = form.save()

        return super(ShiftViewSaveMixin, self).form_valid(form)

class ShiftCreateView(ShiftViewSaveMixin, CreateView):
    template_name = 'organizations/shift_form.html'
    model = Shift
    form_class = ShiftForm
    success_url = '/shifts/'

    def get_context_data(self, **kwargs):
        data = super(ShiftCreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            data['task_form'] = TaskForm(self.request.POST)
        else:
            data['task_form'] = TaskForm()
        return data

class ShiftUpdateView(ShiftViewSaveMixin, UpdateView):
    """
    TODO: access permission needs to be checked before data gets updated in DB.
    """

    slug_field = 'id'
    slug_url_kwarg = 'id'
    template_name = 'organizations/shift_form.html'
    model = Shift
    form_class = ShiftForm
    success_url = '/shifts/'

    def get_context_data(self, **kwargs):
        data = super(ShiftUpdateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            data['task_form'] = TaskForm(self.request.POST)
        else:
            form = self.get_form()
            data['task_form'] = TaskForm(instance=form.instance.task)
        return data


# ------------------------------------------------------------------------------
@login_required()
def shift_delete(request, shift_id):
    context = {}

    # TODO: not implemented
    return render(request, 'organizations/shift_edit.html', context)

