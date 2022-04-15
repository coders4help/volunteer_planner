from datetime import date, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from registration.models import RegistrationProfile


class Command(BaseCommand):
    help = "Cleanup expired registrations"

    def handle(self, *args, **options):
        profiles = (
            RegistrationProfile.objects.exclude(activated=True)
            .prefetch_related("user", "user__account")
            .exclude(user__is_active=True)
            .filter(
                user__date_joined__lt=(
                    date.today() - timedelta(settings.ACCOUNT_ACTIVATION_DAYS)
                )
            )
        )

        if settings.DEBUG:
            self.stderr.write("SQL: {}".format(profiles.query))

        for profile in profiles:
            if hasattr(profile, "user"):
                if hasattr(profile.user, "account"):
                    profile.user.account.delete()
                profile.user.delete()
            profile.delete()
