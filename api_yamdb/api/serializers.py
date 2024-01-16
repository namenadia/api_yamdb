from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers

from reviews.models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title',)
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('user', 'title'),
                message='Вы уже оставили отзыв с оценкой'
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)
