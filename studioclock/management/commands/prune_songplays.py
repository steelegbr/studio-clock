from calendar import monthrange
from datetime import UTC, datetime

from django.core.management import BaseCommand

from studioclock.models import SongPlay


class Command(BaseCommand):
    help = "Delete SongPlay records older than the retention period."

    def add_arguments(self, parser):
        parser.add_argument(
            "--months",
            type=int,
            default=6,
            help="Retention period in calendar months (default: 6).",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Report the number of records that would be deleted.",
        )

    def handle(self, *args, **options):
        months = options["months"]

        if months < 1:
            self.stderr.write("Retention period must be at least one month.")
            return

        cutoff = self.months_ago(datetime.now().astimezone(UTC), months)

        expired = SongPlay.objects.filter(timestamp__lt=cutoff)
        count = expired.count()

        if options["dry_run"]:
            self.stdout.write(
                f"Would delete {count} SongPlay records older than {cutoff}."
            )
            return

        _, deleted_by_model = expired.delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"Deleted {deleted_by_model.get('studioclock.SongPlay', 0)} "
                f"SongPlay records older than {cutoff}."
            )
        )

    @staticmethod
    def months_ago(date, months):
        month_index = date.month - 1 - months
        year = date.year + month_index // 12
        month = month_index % 12 + 1
        day = min(date.day, monthrange(year, month)[1])

        return date.replace(year=year, month=month, day=day)
