
from django.core.validators import RegexValidator
from django.db import models


class BaseModel(models.Model):
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)


class CategoryGenreBaseModel(models.Model):
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
