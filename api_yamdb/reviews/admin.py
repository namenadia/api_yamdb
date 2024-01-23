from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


admin.site.empty_value_display = 'Не задано'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Класс настройки Категорий."""

    list_display = (
        'pk',
        'name',
        'slug',
    )
    list_editable = ('name', 'slug')
    list_filter = ('slug',)
    search_fields = ('name',)


@admin.register(Genre)
class GenereAdmin(CategoryAdmin):
    """Класс настройки Жанров."""
    pass


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Класс настройки Произведений."""

    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'category'
    )
    filter_horizontal = ('genre',)
    list_editable = ('name', 'description', 'year', 'category')
    list_filter = ('year', 'category')
    search_fields = ('name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Класс настройки Произведений."""

    list_display = (
        'pk',
        'author',
        'text',
        'score',
        'title'
    )
    list_editable = ('text', 'score', 'title')
    list_filter = ('author', 'title')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Класс настройки Произведений."""

    list_display = (
        'pk',
        'author',
        'text',
        'review'
    )
    list_editable = ('text',)
    list_filter = ('author',)
