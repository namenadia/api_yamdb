from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import ValidateUsername


class User(AbstractUser):
    """Класс пользователей."""
    
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLES = (
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    )

    username = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
        unique=True,
        db_index=True,
        validators=[ValidateUsername]
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='Email',
        unique=True
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        blank=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )
    role = models.CharField(
        max_length=20,
        verbose_name='Роль',
        choices=ROLES,
        default=USER,
    )
    confirmation_code = models.CharField(
        verbose_name='confirmation_code',
        max_length=50,
        blank=True,
        default=0
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username='me'), name='name_not_me')
        ]

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        if self.role == User.ADMIN or self.is_staff or self.is_superuser:
            User.is_staff = True
            User.is_superuser = True
            User.save(self)
            return User

    @property
    def is_moderator(self):
        return self.role == 'moderator'
