from statistics import mean

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from .validators import ValidateUsername, ValidateTitle


class UserSerializer(serializers.ModelSerializer, ValidateUsername):
    """Сериализатор модели User."""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        lookup_field = ('username',)


class RegistrationSerializer(serializers.Serializer, ValidateUsername):
    """Сериализатор регистрации User."""

    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True, max_length=254)


class TokenSerializer(serializers.Serializer, ValidateUsername):
    """Сериализатор токена."""

    username = serializers.CharField(required=True, max_length=150)
    confirmation_code = serializers.CharField(required=True)


class UserEditSerializer(UserSerializer):
    """Сериализатор модели User для get и patch."""

    role = serializers.CharField(read_only=True)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор модели Category."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор модели Genre."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleRSerializer(serializers.ModelSerializer):
    """Сериализатор модели Title для GET запросов."""

    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Title

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        return round(
            mean(review.score for review in reviews)
        ) if reviews else None


class TitleCUDSerializer(serializers.ModelSerializer, ValidateTitle):
    """Сериализатор модели Title для небезопасных запросов."""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели Review."""

    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title',)
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title'),
                message='Вы уже оставили отзыв с оценкой'
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели Comment."""

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)
