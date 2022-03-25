from django import forms
from django.core.validators import RegexValidator
from django.utils.text import gettext_lazy as _

from registration.forms import RegistrationFormUniqueEmail

username_first_char_validator = RegexValidator(
    r"^[a-zA-Z]", _("Username must start with a letter.")
)
username_validator = RegexValidator(
    r"^[a-zA-Z0-9_.]*$",
    _('Invalid username. Allowed characters are letters, numbers, "." and "_".'),
)
username_last_char_validator = RegexValidator(
    r"[a-zA-Z0-9]$", _("Username must end with a letter or a number.")
)
no_consequtive_dots = RegexValidator(
    r"\.\.",
    _("Username must not contain consecutive . or _ characters."),
    inverse_match=True,
)
no_consequtive_underscores = RegexValidator(
    r"__",
    _("Username must not contain consecutive . or _ characters."),
    inverse_match=True,
)
no_consequtive_funnystuff = RegexValidator(
    r"_\.",
    _("Username must not contain consecutive . or _ characters."),
    inverse_match=True,
)
no_consequtive_funnystuff2 = RegexValidator(
    r"\._",
    _("Username must not contain consecutive . or _ characters."),
    inverse_match=True,
)


class RegistrationForm(RegistrationFormUniqueEmail):

    username = forms.CharField(
        max_length=16,
        min_length=3,
        strip=False,
        validators=[
            username_first_char_validator,
            username_validator,
            username_last_char_validator,
            no_consequtive_dots,
            no_consequtive_underscores,
            no_consequtive_funnystuff,
            no_consequtive_funnystuff2,
        ],
    )

    accept_privacy_policy = forms.BooleanField(
        required=True, initial=False, label=_("Accept privacy policy")
    )
