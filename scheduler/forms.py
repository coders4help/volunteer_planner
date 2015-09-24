# coding: utf-8

from django import forms

from scheduler.models import Need


class RegisterForNeedForm(forms.Form):
    leave_shift = forms.ModelChoiceField(queryset=Need.objects, required=False)
    join_shift = forms.ModelChoiceField(queryset=Need.objects, required=False)
