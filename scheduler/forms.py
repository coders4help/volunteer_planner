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
        fields = ['workplace', 'slots', 'starting_time', 'ending_time', ]
        help_texts = {
            #'starting_time': 'Date/Time Format: YYYY-MM-DD HH:MM',
        }
        widgets = {
            'workplace': forms.Select({'class': 'form-control'}),
            'starting_time': widgets.AdminSplitDateTime({'class': 'form-control'}),
            'ending_time': widgets.AdminSplitDateTime({'class': 'form-control'}),
            'slots': forms.NumberInput({'class': 'form-control'}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['facility', 'name', 'description', ]
        labels = {
            'name': 'Task'
        }
        widgets = {
            'facility': forms.Select({'class': 'form-control'}),
            'name': forms.TextInput({'class': 'form-control'}),
            'description': forms.Textarea({'class': 'form-control'}),
        }
