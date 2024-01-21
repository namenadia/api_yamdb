from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import real_score
from core.models import ReviewCommentBaseModel, CategoryGenreBaseModel

User = get_user_model()


class Category(CategoryGenreBaseModel):
    """Модель для категории."""

    class Meta(CategoryGenreBaseModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:settings.SHORT_NAME]


class Genre(CategoryGenreBaseModel):
    """Модель для жанра."""

    class Meta(CategoryGenreBaseModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:settings.SHORT_NAME]


class Title(models.Model):
    """Модель для произведения."""

    name = models.CharField('Название', max_length=256)
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
        validators=[
            MinValueValidator(
                0,
                message='Значение года не может быть отрицательным'
            ),
            MaxValueValidator(
                int(datetime.now().year),
                message='Значение года не может быть больше текущего'
            )
        ],
    )
    description = models.TextField('Описание', blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='categories',
        blank=True,
        null=True,
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre',
        related_name='genres',
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name[:settings.SHORT_NAME]


class TitleGenre(models.Model):
    """Промежуточная модель соответсвия произведений и жанров."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Жанр'
    )

    def __str__(self):
        return f'{self.title} - {self.genre}'


class Review(ReviewCommentBaseModel):
    """Модель для отзыва."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField('Текст Отзыва')
    score = models.PositiveSmallIntegerField(
        'Рейтинг',
        validators=(real_score,),
        help_text=(
            'Оцените произведение по шкале от 1 до 10.'
        )
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        blank=True,
        null=True
    )

    class Meta(ReviewCommentBaseModel.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:settings.SHORT_NAME]


class Comment(ReviewCommentBaseModel):
    """Модель для комментария."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField('Текст Коментария')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta(ReviewCommentBaseModel.Meta):
        verbose_name = 'Комментрарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:settings.SHORT_NAME]
