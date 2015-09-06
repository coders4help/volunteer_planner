from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class BluePrintCreator(models.Model):
    class Meta:
        verbose_name = "Vorlage"
        verbose_name_plural = "Vorlagen"

    title = models.CharField(verbose_name="Name der Vorlage", max_length=255)
    location = models.ForeignKey('scheduler.Location', verbose_name="Ort")
    needs = models.ManyToManyField('NeedBluePrint', verbose_name="Schichten")

    def __unicode__(self):
        return self.title


class NeedBluePrint(models.Model):
    class Meta:
        verbose_name = "Schicht Vorlage"
        verbose_name_plural = "Schicht Vorlagen"

    topic = models.ForeignKey('scheduler.Topics', verbose_name="Hilfetyp")
    from_time = models.CharField(verbose_name='Uhrzeit von', max_length=5)
    to_time = models.CharField(verbose_name='Uhrzeit bis', max_length=5)
    slots = models.IntegerField(verbose_name="Anz. benoetigter Freiwillige")

    def get_location(self):
        return self.blueprintcreator_set.all().get().location

    def __unicode__(self):
        try:
            location_name = self.blueprintcreator_set.all().get().location.name
        except:
            location_name=""
        return self.topic.title +" von "+self.from_time + " bis "+ self.to_time + " "+location_name



