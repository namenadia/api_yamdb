from django.core.validators import RegexValidator
from django.db import models


class PubDateBaseModel(models.Model):
    """Абстрактная модель с полем pub_date."""

    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)


class NameSlugBaseModel(models.Model):
    """Абстрактная модель с полями name и slug."""

    name = models.CharField('Название', max_length=256)
    slug = models.SlugField(
        'Слаг',
        max_length=50,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Слаг содержит недопустимый символ'
        )]
    )

    class Meta:
        abstract = True
        ordering = ('name',)
