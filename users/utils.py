from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_welcome_email(user_email, user_name=None):
    """
    Отправка приветственного письма пользователю после регистрации

    Args:
        user_email (str): Email пользователя
        user_name (str, optional): Имя пользователя
    """

    # Если имя не указано, используем email
    if not user_name:
        user_name = user_email.split('@')[0]

    # Контекст для шаблона
    context = {
        'user_name': user_name,
        'user_email': user_email,
        'site_name': 'Мой сайт',
        'site_url': 'http://localhost:8000',
    }

    # Рендерим HTML шаблон письма
    html_message = render_to_string('users/emails/welcome_email.html', context)

    # Создаем текстовую версию письма
    plain_message = strip_tags(html_message)

    # Отправляем письмо
    send_mail(
        subject='Добро пожаловать на наш сайт!',
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        html_message=html_message,
        fail_silently=False,
    )


def send_password_reset_email(user, reset_link):
    """
    Отправка письма для восстановления пароля
    """
    context = {
        'user': user,
        'reset_link': reset_link,
        'site_name': 'Мой сайт',
    }

    html_message = render_to_string('users/emails/password_reset_email.html', context)
    plain_message = strip_tags(html_message)

    send_mail(
        subject='Восстановление пароля',
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )