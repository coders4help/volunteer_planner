# coding: utf-8

import factory

from scheduler import models as scheduler_models


class TopicFactory(factory.DjangoModelFactory):
    class Meta:
        model = scheduler_models.Topics


class LocationFactory(factory.DjangoModelFactory):
    class Meta:
        model = scheduler_models.Location


class NeedFactory(factory.DjangoModelFactory):
    topic = factory.SubFactory(TopicFactory)
    location = factory.SubFactory(LocationFactory)

    slots = 10

    class Meta:
        model = scheduler_models.Need
