from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .utils import current_year
from core.models import PubDateBaseModel, NameSlugBaseModel

User = get_user_model()


class Category(NameSlugBaseModel):
    """Модель для категории."""

    class Meta(NameSlugBaseModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:settings.SHORT_NAME]


class Genre(NameSlugBaseModel):
    """Модель для жанра."""

    class Meta(NameSlugBaseModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:settings.SHORT_NAME]


class Title(models.Model):
    """Модель для произведения."""

    name = models.CharField('Название', max_length=256)
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
        validators=[current_year, ],
    )
    description = models.TextField('Описание', blank=True)
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
        related_name='genres',
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name[:settings.SHORT_NAME]


class Review(PubDateBaseModel):
    """Модель для отзыва."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    text = models.TextField('Текст Отзыва')
    score = models.PositiveSmallIntegerField(
        'Рейтинг',
        validators=[
            MinValueValidator(
                limit_value=settings.MIN_VALUE_SCORE,
                message=('Значение оценки не может быть '
                         f'меньше {settings.MIN_VALUE_SCORE}')
            ),
            MaxValueValidator(
                limit_value=settings.MAX_VALUE_SCORE,
                message=('Значение оценки не может быть '
                         f'больше {settings.MAX_VALUE_SCORE}')
            )
        ],
        help_text=(
            'Оцените произведение по шкале от 1 до 10.'
        )
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    class Meta(PubDateBaseModel.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = "reviews"
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]

    def __str__(self):
        return self.text[:settings.SHORT_NAME]


class Comment(PubDateBaseModel):
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

    class Meta(PubDateBaseModel.Meta):
        verbose_name = 'Комментрарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:settings.SHORT_NAME]
