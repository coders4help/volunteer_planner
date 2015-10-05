# coding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _

class BluePrintCreator(models.Model):
    class Meta:
        verbose_name = _("Blueprint")
        verbose_name_plural = _("Blueprints")

    title = models.CharField(verbose_name=_("blueprint title"), max_length=255)
    location = models.ForeignKey('scheduler.Location', verbose_name=_("location"))
    needs = models.ManyToManyField('NeedBluePrint', verbose_name=_("shifts"))

    def __unicode__(self):
        return u'{}'.format(self.title)


class NeedBluePrint(models.Model):
    class Meta:
        verbose_name = _("Blueprint Item")
        verbose_name_plural = _("Blueprint Items")

    topic = models.ForeignKey('scheduler.Topics', verbose_name=_("topic"))
    from_time = models.CharField(verbose_name=_('from hh:mm'), max_length=5)
    to_time = models.CharField(verbose_name=_('until hh:mm'), max_length=5)
    slots = models.IntegerField(verbose_name=_("number of volunteers needed"))

    def get_location(self):
        return self.blueprintcreator_set.all().get().location

    def __unicode__(self):
        try:
            location_name = u' ({})'.format(self.blueprintcreator_set.all().get().location.name)
        except:
            location_name = u''

        return u'{} von {} bis {}{}'.format(self.topic.title, self.from_time, self.to_time, location_name)
