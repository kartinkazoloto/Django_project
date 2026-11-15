from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAuthTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="StrongPass123!",
        )

    def test_login_page_renders(self):
        """Страница входа открывается без NoReverseMatch."""
        response = self.client.get(reverse("users:login"))
        self.assertEqual(response.status_code, 200)

    def test_login_by_email_success(self):
        """Успешный вход по email."""
        response = self.client.post(
            reverse("users:login"),
            {"username": "test@example.com", "password": "StrongPass123!"},
        )
        self.assertEqual(response.status_code, 302)  # редирект после входа

    def test_login_wrong_password_shows_error(self):
        """Неверный пароль — понятная ошибка, пользователь не авторизован."""
        response = self.client.post(
            reverse("users:login"),
            {"username": "test@example.com", "password": "wrong"},
            follow=True,
        )
        self.assertContains(response, "неверно", status_code=200)
        self.assertFalse(response.context["user"].is_authenticated)

    def test_closed_page_requires_login(self):
        """Закрытая страница недоступна без авторизации."""
        response = self.client.get(reverse("catalog:product_list"))
        # Должен быть редирект на login, если используется LoginRequiredMixin
        self.assertIn(response.status_code, (302, 403))


class UserRegistrationTests(TestCase):

    def test_registration_sends_email(self):
        """После регистрации отправляется письмо."""
        response = self.client.post(
            reverse("users:register"),
            {
                "email": "new@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("new@example.com", mail.outbox[0].to)