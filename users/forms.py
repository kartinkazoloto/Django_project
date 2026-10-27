from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


class CustomUserCreationForm(forms.ModelForm):
    """Форма для регистрации пользователя"""

    email = forms.EmailField(
        label=_('Email'),
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш email',
            'autocomplete': 'email'
        }),
        validators=[validate_email]
    )

    password1 = forms.CharField(
        label=_('Пароль'),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль (мин. 8 символов)',
            'autocomplete': 'new-password'
        }),
        help_text='Пароль должен содержать минимум 8 символов'
    )

    password2 = forms.CharField(
        label=_('Подтверждение пароля'),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтвердите пароль',
            'autocomplete': 'new-password'
        }),
    )

    class Meta:
        model = CustomUser
        fields = ('email',)

    def clean_email(self):
        """Проверка, что email уникален"""
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует.')
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1:
            validate_password(password1, self.instance)
        return password1


    def clean_password2(self):
        """Проверка совпадения паролей"""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпадают.')

        if password1 and len(password1) < 8:
            raise forms.ValidationError('Пароль должен содержать минимум 8 символов.')

        return password2

    def save(self, commit=True):
        """Сохранение пользователя с хешированным паролем"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """Форма для авторизации пользователя по email"""

    username = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш email',
            'autocomplete': 'email'
        })
    )

    password = forms.CharField(
        label=_('Пароль'),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль',
            'autocomplete': 'current-password'
        }),
    )

    error_messages = {
        'invalid_login': _(
            'Неверный email или пароль. Пожалуйста, проверьте введенные данные.'
        ),
        'inactive': _('Эта учетная запись неактивна.'),
    }

    def clean(self):
        """Проверка учетных данных"""
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(
                self.request,
                username=email,
                password=password
            )

            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

class CustomUserChangeForm(forms.ModelForm):
    """Форма редактирования профиля"""

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone_number', 'avatar', 'country')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }