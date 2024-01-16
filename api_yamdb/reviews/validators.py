from django.core.exceptions import ValidationError


def real_score(value):
    if value < 1 or value > 10:
        raise ValidationError(
            'Ожидается рейтинг от 1 до 10'
        )
