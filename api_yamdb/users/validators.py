import re

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError


class ValidateUsername(UnicodeUsernameValidator):
    """Валидаторы для username."""

    def validate_username(self, username):
        pattern = re.compile(r'^[\w.@+-]+')

        if pattern.fullmatch(username) is None:
            match = re.split(pattern, username)
            symbol = ''.join(match)
            raise ValidationError(f'Некорректные символы в username: {symbol}')
        if username == 'me':
            raise ValidationError('Ник "me" нельзя регистрировать!')
        return username
