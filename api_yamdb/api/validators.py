import re

from django.core.exceptions import ValidationError
from rest_framework import serializers

from reviews.models import Category, Genre


class ValidateUsername:
    """Валидаторы для username."""

    def validate_username(self, username):
        pattern = re.compile(r'^[\w.@+-]+')

        if pattern.fullmatch(username) is None:
            match = re.split(pattern, username)
            symbol = ''.join(match)
            raise ValidationError(f'Некорректные символы в username: {symbol}')
        if username == 'me':
            raise ValidationError('Ник "me" нельзя регистрировать!')
        return username


class ValidateTitle:
    """Валидаторы категории и жанра для Title."""

    def validate_category(self, value):
        if not Category.objects.filter(id=value.id).exists():
            raise serializers.ValidationError('Категория не существует')
        return value

    def validate_genre(self, value):
        for genre in value:
            if not Genre.objects.filter(id=genre.id).exists():
                raise serializers.ValidationError('Жанр не существует')
        return value
