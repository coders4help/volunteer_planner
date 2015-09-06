from django.db import models


class Mailer(models.Model):
    location = models.ForeignKey("scheduler.Location")
    first_name = models.CharField(verbose_name='Vorname', max_length=255)
    last_name = models.CharField(verbose_name='Nachname', max_length=255)
    position = models.CharField(verbose_name='Position', max_length=255)
    organization = models.CharField(verbose_name='Organisation', max_length=255)
    email = models.EmailField(verbose_name='Email')

    def __unicode__(self):
        return self.organization +"("+self.location.name+")"