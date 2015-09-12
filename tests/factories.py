# -*- coding: utf-8 -*-
import factory

from scheduler import models as scheduler_models


class TopicFactory(factory.DjangoModelFactory):

    class Meta:
        model = scheduler_models.Topics


class LocationFactory(factory.DjangoModelFactory):

    class Meta:
        model = scheduler_models.Location


class TimePeriodFactory(factory.DjangoModelFactory):

    class Meta:
        model = scheduler_models.TimePeriods


class NeedFactory(factory.DjangoModelFactory):
    topic = factory.SubFactory(TopicFactory)
    location = factory.SubFactory(LocationFactory)
    time_period_from = factory.SubFactory(TimePeriodFactory)
    time_period_to = factory.SubFactory(TimePeriodFactory)

    slots = 10

    class Meta:
        model = scheduler_models.Need
