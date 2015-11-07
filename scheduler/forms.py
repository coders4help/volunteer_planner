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
            'starting_time': forms.DateTimeInput({'class': 'form-control',
                                                  'placeholder': 'YYYY-MM-DD HH:MM'}),
            'ending_time': forms.DateTimeInput({'class': 'form-control',
                                                'placeholder': 'YYYY-MM-DD HH:MM'}),
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

ShiftFormSet = forms.inlineformset_factory(Task, Shift,
                                           form=ShiftForm, extra=2,
                                           min_num=1, validate_min=True,
                                           can_delete=False)