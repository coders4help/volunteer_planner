from datetime import timedelta
from django.db import models


class EnrolmentManager(models.Manager):

    def conflicting(self, shift, user_account=None, grace=timedelta(hours=1)):

        grace = grace or timedelta(0)
        graced_start = shift.starting_time + grace
        graced_end = shift.ending_time - grace

        query_set = self.get_queryset().select_related('shift', 'user_account')

        if user_account:
            query_set = query_set.filter(user=user_account)

        query_set = query_set.exclude(shift__start_time__lt=graced_start,
                                      shift__end_time__lte=graced_start)
        query_set = query_set.exclude(shift__start_time__gte=graced_end,
                                      shift__end_time__gte=graced_end)
        return query_set
