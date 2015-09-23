from django.conf import settings
from django.db import models

from django.utils.translation import ugettext_lazy as _

MANAGED = False


class OldRegistrationProfileNeed(models.Model):
    registrationprofile = models.ForeignKey('OldRegistrationProfile')
    need = models.ForeignKey('scheduler.Need')

    class Meta:
        managed = MANAGED
        db_table = 'registration_registrationprofile_needs'


class OldRegistrationProfile(models.Model):
    class Meta:
        managed = MANAGED
        db_table = 'registration_registrationprofile'

    ACTIVATED = u"ALREADY_ACTIVATED"

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                verbose_name=_('user'))
    activation_key = models.CharField(_('activation key'), max_length=40)

    needs = models.ManyToManyField('scheduler.Need',
                                   verbose_name="registrierte Schichten",
                                   through='OldRegistrationProfileNeed')
