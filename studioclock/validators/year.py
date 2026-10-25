from datetime import datetime

from django.core.exceptions import ValidationError


def valid_year(value):
    current_year = datetime.now().year
    if value <= 0 or value > current_year + 5:
        raise ValidationError(
            f"Year must be between 0 and {current_year + 5}", code="year_out_of_range"
        )
