from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title
from users.validators import validate_username

from .utils import send_confirmation_code, give_confirmation_code

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User."""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        lookup_field = ('username',)


class RegistrationSerializer(serializers.Serializer):
    """Сериализатор регистрации User."""

    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[validate_username]
    )
    email = serializers.EmailField(
        required=True,
        max_length=254
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        try:
            user = User.objects.get(username=username, email=email)
            confirmation_code = give_confirmation_code(user)
            send_confirmation_code(validated_data['email'], confirmation_code)
        except ObjectDoesNotExist:
            serializers = UserSerializer(data=validated_data)
            serializers.is_valid(raise_exception=True)
            user = User(
                username=validated_data['username'],
                email=validated_data['email']
            )
            user.save()
        return user


class TokenSerializer(serializers.Serializer):
    """Сериализатор токена."""

    username = serializers.CharField(required=True, max_length=150)
    confirmation_code = serializers.CharField(max_length=50, required=True)


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
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title


class TitleCUDSerializer(serializers.ModelSerializer):
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
    rating = serializers.IntegerField(read_only=True, default=None)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['category'] = {
            'name': (get_object_or_404(Category, slug=ret['category'])).name,
            'slug': ret['category']}
        genre = []
        for genre_slug in ret['genre']:
            genre.append({
                'name': (get_object_or_404(Genre, slug=genre_slug)).name,
                'slug': genre_slug})
        ret['genre'] = genre
        return ret


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели Review."""

    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        if self.context.get('request').method == 'POST':
            author = self.context.get('request').user
            title_id = self.context.get('view').kwargs.get('title_id')
            title = get_object_or_404(Title, id=title_id)
            if Review.objects.filter(title_id=title.id,
                                     author=author).exists():
                raise ValidationError('Может существовать только один отзыв!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели Comment."""

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
