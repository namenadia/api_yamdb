from django.core.exceptions import ValidationError
from django.utils import timezone


def current_year(value):
    now = timezone.now().year
    if value > now:
        raise ValidationError(
            f'{value} не может быть больше {now}'
        )
