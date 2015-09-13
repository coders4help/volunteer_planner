"""
This app is mainly for storing values of saving calculations to display
on the website.
For instance the management command in scheudler "calculate_volunteer_hours"
calculates shifts every 12 hours and makes results persistent in DB
"""

from django.db import models


class ValueStore(models.Model):

    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name