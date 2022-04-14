from django import forms
from django.core.exceptions import ValidationError
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
    _('Username must not contain consecutive "." or "_" characters.'),
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

    email = forms.EmailField(label=_("e-mail address"))
    email2 = forms.EmailField(label=_("repeat e-mail address"))

    accept_privacy_policy = forms.BooleanField(
        required=True, initial=False, label=_("Accept privacy policy")
    )

    def clean_email2(self):
        email = self.cleaned_data.get("email")
        email2 = self.cleaned_data.get("email2")
        if email and email2 and email != email2:
            raise ValidationError(
                _("The two e-mail addresses didn’t match."),
                code="email_mismatch",
            )
        return email2
