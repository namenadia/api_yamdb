from rest_framework import serializers

from reviews.models import Category, Genre, Title
from .validators import year_not_future, existing_category, existing_genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        year_not_future(value)
        return value

    def validate_category(self, value):
        existing_category(value)
        return value

    def validate_genre(self, value):
        existing_genre(value)
        return value
