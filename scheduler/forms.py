# coding: utf-8

from django import forms

from scheduler.models import Shift


class RegisterForShiftForm(forms.Form):
    leave_shift = forms.ModelChoiceField(queryset=Shift.objects, required=False)
    join_shift = forms.ModelChoiceField(queryset=Shift.objects, required=False)
