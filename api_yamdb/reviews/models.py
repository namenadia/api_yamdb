from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils import timezone

from .validators import real_score
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
        validators=[
            MaxValueValidator(
                timezone.now().year,
                message='Значение года не может быть больше текущего'
            )
        ],
    )
    description = models.TextField('Описание', blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='categories',
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
        validators=(real_score,),
        help_text=(
            'Оцените произведение по шкале от 1 до 10.'
        )
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        blank=True,
        null=True
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
