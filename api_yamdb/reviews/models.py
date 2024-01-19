from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from core.models import BaseModel
from .validators import real_score

User = get_user_model()


class Title(models.Model):
    name = models.TextField()


class Review(BaseModel):
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
        related_name='titles',
        blank=True,
        null=True
    )

    class Meta(BaseModel.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:settings.SHORT_NAME]


class Comment(BaseModel):
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

    class Meta(BaseModel.Meta):
        verbose_name = 'Комментрарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:settings.SHORT_NAME]
