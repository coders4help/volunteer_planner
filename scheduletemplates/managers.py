# coding: utf-8
from django.db import models
from django.db.models import F


class ShiftTemplateManager(models.Manager):
    def get_queryset(self):
        qs = super(ShiftTemplateManager, self).get_queryset()
        qs = qs.select_related(
            "task",
            "task__facility",
            "workplace",
            "workplace__facility",
            "schedule_template",
            "schedule_template__facility",
        )

        qs = qs.order_by(
            "schedule_template",
            F("task__priority").desc(nulls_last=True),
            F("workplace__priority").desc(nulls_last=True),
            "starting_time",
            "-days",
            "-ending_time",
        )
        return qs
