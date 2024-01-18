from statistics import mean

from rest_framework import serializers

from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Title

    def validate_category(self, value):
        if not Category.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Категория не существует")
        return value

    def validate_genre(self, value):
        if not Genre.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Жанр не существует")
        return value

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        return mean(review.score for review in reviews) if reviews else None
