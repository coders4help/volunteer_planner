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
        self.stdout.write('Deleting expired user registrations')
        dry_run = True if self.OPT_SIMULATE in options and options[self.OPT_SIMULATE] else False
        RegistrationProfile.objects.delete_expired_users(dry_run)
