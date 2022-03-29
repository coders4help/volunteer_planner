from django import forms
from django.core.validators import RegexValidator
from django.utils.text import gettext_lazy as _

from registration.forms import RegistrationFormUniqueEmail

username_validator = RegexValidator(
    r"[^\w.]",
    _('Invalid username. Allowed characters are letters, numbers, "." and "_".'),
    inverse_match=True,
)
username_first_char_validator = RegexValidator(
    r"^[\d_.]", _("Username must start with a letter."), inverse_match=True
)
username_last_char_validator = RegexValidator(
    r"[\w]$", _('Username must end with a letter, a number or "_".')
)
no_consequtive = RegexValidator(
    r"[_.]{2,}",
    _("Username must not contain consecutive . or _ characters."),
    inverse_match=True,
)


class RegistrationForm(RegistrationFormUniqueEmail):

    username = forms.CharField(
        max_length=32,
        min_length=3,
        strip=False,
        validators=[
            username_validator,
            username_first_char_validator,
            username_last_char_validator,
            no_consequtive,
        ],
    )

    accept_privacy_policy = forms.BooleanField(
        required=True, initial=False, label=_("Accept privacy policy")
    )
