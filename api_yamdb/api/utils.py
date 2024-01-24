from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator

from api_yamdb.settings import DEFAULT_FROM_EMAIL


def send_confirmation_code(email, confirmation_code):
    """Oтправляет на почту пользователя код подтверждения."""
    send_mail(
        subject='Регистрация в проекте YaMDb.',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[email]
    )


def give_and_save_confirmation_code(user):
    """Сохраняет код в базе данных."""
    confirmation_code = default_token_generator.make_token(user)
    user.confirmation_code = confirmation_code
    user.save()
