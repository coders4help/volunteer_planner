# coding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _


class BluePrintCreator(models.Model):
    class Meta:
        verbose_name = "Vorlage"
        verbose_name_plural = "Vorlagen"

    title = models.CharField(verbose_name="Name der Vorlage", max_length=255)
    facility = models.ForeignKey('organizations.Facility',
                                 verbose_name=_('facility'))
    needs = models.ManyToManyField('NeedBluePrint', verbose_name=_('shifts'))

    def __unicode__(self):
        return u'{}'.format(self.title)


class NeedBluePrint(models.Model):
    class Meta:
        verbose_name = "Schicht Vorlage"
        verbose_name_plural = "Schicht Vorlagen"

    topic = models.ForeignKey('scheduler.Topics', verbose_name="Hilfetyp")
    from_time = models.CharField(verbose_name='Uhrzeit von', max_length=5)
    to_time = models.CharField(verbose_name='Uhrzeit bis', max_length=5)
    slots = models.IntegerField(verbose_name="Anz. benoetigter Freiwillige")

    def get_facility(self):
        return self.blueprintcreator_set.all().get().facility

    def __unicode__(self):
        try:
            facility_name = u' ({})'.format(
                self.blueprintcreator_set.all().get().facility.name)
        except:
            facility_name = u''

        return u'{} von {} bis {}{}'.format(self.topic.title, self.from_time,
                                            self.to_time, facility_name)
