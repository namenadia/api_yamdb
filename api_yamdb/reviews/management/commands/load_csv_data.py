import csv

from django.conf import settings
from django.core.management import BaseCommand
from django.db import connection

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

csv_list = [
    'users',
    'category',
    'genre',
    'titles',
    'review',
    'comments',
    'genre_title',
]

csv_models = {
    'category': Category,
    'comments': Comment,
    'genre': Genre,
    'review': Review,
    'titles': Title,
    'users': User,
    'author': User,
}


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for csv_f in csv_list:
            with open(
                str(settings.BASE_DIR) + '/static/data/' + csv_f + '.csv',
                'r',
                encoding='utf-8',
            ) as csv_file:
                for data in csv.DictReader(csv_file):
                    if csv_f == 'genre_title':
                        cursor = connection.cursor()
                        title_id = data['title_id']
                        genre_id = data['genre_id']
                        cursor.execute(
                            'INSERT INTO reviews_title_genre '
                            f'(title_id, genre_id) VALUES ({title_id}, '
                            f'{genre_id})'
                        )
                        cursor.close()
                        connection.close()
                    else:
                        for key, value in data.items():
                            if key in csv_models:
                                data[key] = csv_models[key].objects.get(
                                    pk=value
                                )
                        model = csv_models.get(csv_f)(**data)
                        model.save()
        self.stdout.write(self.style.SUCCESS('Данные загружены'))
