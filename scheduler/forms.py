# coding: utf-8

from django import forms
from django.contrib.admin import widgets

from organizations.models import Task
from scheduler.models import Shift


class RegisterForShiftForm(forms.Form):
    leave_shift = forms.ModelChoiceField(queryset=Shift.objects, required=False)
    join_shift = forms.ModelChoiceField(queryset=Shift.objects, required=False)

class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ['workplace', 'starting_time', 'ending_time', 'slots', ]
        widgets = {
            'starting_time': widgets.AdminSplitDateTime,
            'ending_time': widgets.AdminSplitDateTime,
        }

class TaskForm(forms.ModelForm):
	class Meta:
		model = Task
		exclude = []
