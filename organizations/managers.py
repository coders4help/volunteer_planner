from django.db.models import Q, Count, Manager
from django.utils import timezone


class FacilityManager(Manager):
    def with_open_shifts(self):
        return (
            self.get_queryset()
            .annotate(open_shift_count=Count("shift", filter=Q(shift__ending_time__gte=timezone.now())))
            .exclude(open_shift_count=0)
        )
