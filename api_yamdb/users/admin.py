from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class MyUserAdmin(UserAdmin):
    """Класс настройки раздела пользователей."""

    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role',
        'is_staff',
        'is_superuser',
    )
    list_editable = ('role', 'is_staff', 'is_superuser',)
    list_filter = ('username',)
    search_fields = ('username', 'role')

