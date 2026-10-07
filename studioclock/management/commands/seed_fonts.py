from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from studioclock.data.fonts import FONTS
from studioclock.models import Font, FontWeight


class Command(BaseCommand):
    help = "Seed the application with supported Google Fonts and their weights."

    @atomic
    def handle(self, *args, **options):
        for font_data in FONTS:
            font, created = Font.objects.get_or_create(
                name=font_data["name"],
                family=font_data["family"],
                category=font_data["category"].upper(),
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created font: {font.name}"))
            else:
                self.stdout.write(
                    self.style.WARNING(f"Font already exists: {font.name}")
                )

            for weight_value, weight_name in font_data["weights"]:
                weight, weight_created = FontWeight.objects.get_or_create(
                    font=font,
                    weight=weight_value,
                    name=weight_name,
                )
                if weight_created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  Created weight: {weight.name} ({weight.weight})"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"  Weight already exists: {weight.name} ({weight.weight})"
                        )
                    )
