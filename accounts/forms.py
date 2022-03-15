from django import forms
from registration.forms import RegistrationFormUniqueEmail
from django.utils.text import gettext_lazy as _


class RegistrationForm(RegistrationFormUniqueEmail):
    accept_privacy_policy = forms.BooleanField(required=True, initial=False, label=_("Accept privacy policy"))
