from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator


def send_confirmation_code(email, confirmation_code):
    """Oтправляет на почту пользователя код подтверждения."""
    send_mail(
        subject='Регистрация в проекте YaMDb.',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email]
    )


def give_confirmation_code(user):
    """Сохраняет код в базе данных."""
    return default_token_generator.make_token(user)
