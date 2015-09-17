# coding: utf-8

import factory
from random import randint
import datetime as dt
from scheduler import models as scheduler_models
from factory import DjangoModelFactory, lazy_attribute




def date_random(hours_delta):

    time = dt.datetime.now()+dt.timedelta(hours=hours_delta)
    _time = time.replace(minute=0, second=0, microsecond=0)
    return _time


class TopicFactory(factory.DjangoModelFactory):
    class Meta:
        model = scheduler_models.Topics


class LocationFactory(factory.DjangoModelFactory):
    class Meta:
        model = scheduler_models.Location


class NeedFactory(factory.DjangoModelFactory):
    class Meta:
        model = scheduler_models.Need

    topic = factory.SubFactory(TopicFactory)
    location = factory.SubFactory(LocationFactory)
    starting_time = date_random(hours_delta=1)
    ending_time = date_random(hours_delta=3)

    slots = 10


