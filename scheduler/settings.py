from datetime import timedelta

from django.conf import settings

DEFAULT_SHIFT_CONFLICT_GRACE = getattr(
    settings, "DEFAULT_SHIFT_CONFLICT_GRACE", timedelta(0)
)
