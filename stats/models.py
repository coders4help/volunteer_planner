"""
This app is mainly for storing values of saving calculations to display
on the website.

As far as Maik can tell, it's unused at the moment.
"""

from django.db import models


class ValueStore(models.Model):

    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name
