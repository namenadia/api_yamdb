from rest_framework import serializers

from reviews.models import Category, Genre


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
