from django import forms
from scheduler.models import Need


class RegisterForNeedForm(forms.Form):
    ADD, REMOVE = "add", "remove"
    need = forms.ModelChoiceField(queryset=Need.objects)
    action = forms.ChoiceField(choices=[(ADD, ADD), (REMOVE, REMOVE)])
