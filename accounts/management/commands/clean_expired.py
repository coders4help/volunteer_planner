# coding=utf-8
from django.core.management.base import BaseCommand

from registration.models import RegistrationProfile


class Command(BaseCommand):
    help = 'Cleanup expired registrations'

    OPT_SIMULATE = 'dry-run'

    def add_arguments(self, parser):
        parser.add_argument(''.join(['--', self.OPT_SIMULATE]),
                            action='store_true',
                            dest=self.OPT_SIMULATE,
                            default=False,
                            help='Only print registrations that would be deleted')

    def handle(self, *args, **options):
        dry_run = True if self.OPT_SIMULATE in options and options[
            self.OPT_SIMULATE] else False
        if dry_run:
            user_count, reg_profile_count = 0, 0
            for profile in RegistrationProfile.objects.select_related(
                    'user').exclude(user__is_active=True):
                if profile.activation_key_expired():
                    user_count += 1
                    reg_profile_count += 1
            print "Would delete {} User and {} RegistrationProfile objects".format(
                user_count, reg_profile_count)
        else:
            RegistrationProfile.objects.delete_expired_users()
