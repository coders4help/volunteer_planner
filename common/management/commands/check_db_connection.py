from time import sleep

from django.core.management import BaseCommand, CommandError
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = "This command checks availability of configured database."

    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=5,
            help="Number of connections attempts before failing",
        )
        parser.add_argument(
            "--sleep",
            type=int,
            default=1,
            help="Seconds to wait after every failed attempt",
        )

    def handle(self, *args, **options):
        if 0 > options["count"]:
            raise CommandError(
                "No negative count allowed. It's not I'm picky, "
                "but I simply don't now, how to handle it."
            )
        if 0 > options["sleep"]:
            raise CommandError(
                "No negative sleep allowed. Bear with me, but I forgot my time machine."
            )

        success = False
        db_conn = connections["default"]
        for i in range(0, options["count"]):
            try:
                db_conn.cursor()
                success = True
                break
            except OperationalError as e:
                self.stderr.write(
                    self.style.WARNING("Database connection failed: %s" % e)
                )
                sleep(options["sleep"])

        if not success:
            raise CommandError("Database connection check failed")
