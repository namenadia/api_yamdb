from django.core.exceptions import ValidationError
from django.utils import timezone

from reviews.models import Category, Genre


def year_not_future(value):
    current_year = timezone.now().year
    if value > current_year:
        raise ValidationError('Год выпуска не может быть больше текущего года')


def existing_category(value):
    if not Category.objects.filter(name=value).exists():
        raise ValidationError('Указанная категория не существует')


def existing_genre(value):
    if not Genre.objects.filter(name=value).exists():
        raise ValidationError('Указанный жанр не существует')
