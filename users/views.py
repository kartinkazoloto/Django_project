from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView

import logging

from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserChangeForm
from .models import CustomUser
from .utils import send_welcome_email

logger = logging.getLogger(__name__)

class RegisterView(CreateView):
    """
    Представление для регистрации пользователя
    """
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """Обработка валидной формы регистрации"""
        # Сохраняем пользователя
        user = form.save()

        # Отправляем приветственное письмо
        try:
            send_welcome_email(
                user_email=user.email,
                user_name=user.first_name or user.email.split('@')[0]
            )
            messages.success(
                self.request,
                'Регистрация успешно завершена! На ваш email отправлено приветственное письмо.'
            )
        except Exception:
            logger.exception("Ошибка отправки приветственного письма для %s", user.email)
            messages.warning(
                self.request,
                'Регистрация успешна, но не удалось отправить приветственное письмо.'
            )

        return super().form_valid(form)

    def form_invalid(self, form):
        """Обработка невалидной формы"""
        if form.non_field_errors():
            for error in form.non_field_errors():
                messages.error(self.request, error)
        return super().form_invalid(form)


class CustomLoginView(LoginView):
    """
    Представление для авторизации пользователя по email
    """
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'

    def get_success_url(self):
        """URL для перенаправления после успешного входа"""
        messages.success(self.request, 'Добро пожаловать! Вы успешно вошли в систему.')
        return reverse_lazy('catalog:home')

    def form_invalid(self, form):
        """Обработка невалидной формы входа"""
        messages.error(self.request, 'Неверный email или пароль.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        """Добавление дополнительных данных в контекст"""
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', '')
        return context


class CustomLogoutView(LogoutView):
    """
    Представление для выхода из системы
    """
    next_page = reverse_lazy('users:login')

    def dispatch(self, request, *args, **kwargs):
        """Обработка выхода"""
        messages.info(request, 'Вы вышли из системы.')
        return super().dispatch(request, *args, **kwargs)


@login_required
def profile_view(request):
    """
    Просмотр профиля пользователя
    """
    return render(request, 'users/profile.html', {'user': request.user})


@login_required
def profile_edit_view(request):
    """
    Редактирование профиля пользователя
    """

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('users:profile')
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'users/profile_edit.html', {'form': form})