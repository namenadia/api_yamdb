from django.core.validators import RegexValidator
from django.db import models


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
