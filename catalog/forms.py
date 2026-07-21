import os

from django import forms
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

from config.settings import FORBIDDEN_WORDS, MAX_IMAGE_SIZE, ALLOWED_IMAGE_MIME_TYPES, ALLOWED_IMAGE_EXTENSIONS, \
    MIN_IMAGE_WIDTH, MIN_IMAGE_HEIGHT, MAX_IMAGE_WIDTH, MAX_IMAGE_HEIGHT
from .models import Product, Category




class ProductForm(forms.ModelForm):
    """Форма для создания/редактирования товара с валидацией изображений"""

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label='Категория',
        required=False,
        empty_label='Выберите категорию',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'category-select'
        })
    )

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название товара'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Введите описание товара'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control-file',
                'id': 'product-image',
                'accept': 'image/jpeg,image/png'
            }),
        }
        labels = {
            'name': 'Название товара',
            'description': 'Описание',
            'price': 'Цена (руб.)',
            'image': 'Изображение',
            'category': 'Категория',
        }
        # error_messages = {
        #     'name': {
        #         'required': 'Пожалуйста, введите название товара',
        #     },
        #     'price': {
        #         'required': 'Пожалуйста, укажите цену товара',
        #         'min_value': 'Цена должна быть больше нуля',
        #     },
        # }

    def __init__(self, *args, **kwargs):
        """Единая стилизация всех полей формы"""
        super().__init__(*args, **kwargs)

        base_classes = 'form-control'
        base_error_classes = 'form-control is-invalid'

        for field_name, field in self.fields.items():
            if hasattr(field.widget, 'attrs'):
                current_classes = field.widget.attrs.get('class', '')

                if isinstance(field.widget, forms.FileInput):
                    field.widget.attrs['class'] = 'form-control-file'
                else:
                    if 'form-control' not in current_classes:
                        field.widget.attrs['class'] = f"{current_classes} form-control".strip()

                field.widget.attrs['placeholder'] = field.widget.attrs.get('placeholder', '')

                field.widget.attrs['aria-describedby'] = f"{field_name}-help"

                if field.required:
                    field.widget.attrs['required'] = 'required'

                if isinstance(field.widget, forms.Select):
                    field.widget.attrs['class'] = f"{field.widget.attrs.get('class', '')} form-select".strip()

        self.label_suffix = ':'


    def clean_price(self):
        """Валидация цены"""
        price = self.cleaned_data.get('price')
        if price < 0:
            raise forms.ValidationError('Цена должна быть больше нуля')
        return price

    def clean_name(self):
        """Валидация названия на наличие запрещенных слов"""
        name = self.cleaned_data.get('name')
        if name:
            # Приводим к нижнему регистру для сравнения
            name_lower = name.lower()

            # Проверяем каждое запрещенное слово
            for forbidden_word in FORBIDDEN_WORDS:
                if forbidden_word in name_lower:
                    raise ValidationError(
                        f'Название содержит запрещенное слово: "{forbidden_word}". '
                        f'Пожалуйста, удалите его.'
                    )

            # Проверка на минимальную длину
            if len(name) < 3:
                raise ValidationError('Название должно содержать минимум 3 символа')

        return name

    def clean_description(self):
        """Валидация описания на наличие запрещенных слов"""
        description = self.cleaned_data.get('description')
        if description:
            # Приводим к нижнему регистру для сравнения
            description_lower = description.lower()

            # Проверяем каждое запрещенное слово
            found_words = []
            for forbidden_word in FORBIDDEN_WORDS:
                if forbidden_word in description_lower:
                    found_words.append(forbidden_word)

            if found_words:
                words_str = ', '.join(f'"{word}"' for word in found_words)
                raise ValidationError(
                    f'Описание содержит запрещенные слова: {words_str}. '
                    f'Пожалуйста, удалите их.'
                )

        return description

    def clean_image(self):
        """
        Валидация загружаемого изображения.
        Проверяет формат, размер, размеры изображения.
        """
        image = self.cleaned_data.get('image')

        # Если изображение не загружено, пропускаем валидацию
        if not image:
            return image

        # Проверка размера файла
        if image.size > MAX_IMAGE_SIZE:
            size_in_mb = MAX_IMAGE_SIZE / (1024 * 1024)
            raise ValidationError(
                f'Размер файла превышает {size_in_mb:.0f} МБ. '
                f'Пожалуйста, загрузите файл меньшего размера.'
            )

        # Проверка MIME-типа
        if hasattr(image, 'content_type'):
            if image.content_type not in ALLOWED_IMAGE_MIME_TYPES:
                raise ValidationError(
                    f'Неподдерживаемый формат файла: {image.content_type}. '
                    f'Допустимые форматы: JPEG, PNG.'
                )

        # Проверка расширения файла
        file_extension = os.path.splitext(image.name)[1].lower()
        if file_extension not in ALLOWED_IMAGE_EXTENSIONS:
            raise ValidationError(
                f'Неподдерживаемое расширение файла: {file_extension}. '
                f'Допустимые расширения: {", ".join(ALLOWED_IMAGE_EXTENSIONS)}.'
            )

        # Проверка размеров изображения
        try:
            width, height = get_image_dimensions(image)

            if width is not None and height is not None:
                # Проверка минимальных размеров
                if width < MIN_IMAGE_WIDTH or height < MIN_IMAGE_HEIGHT:
                    raise ValidationError(
                        f'Изображение слишком маленькое. '
                        f'Минимальные размеры: {MIN_IMAGE_WIDTH}x{MIN_IMAGE_HEIGHT} пикселей. '
                        f'Ваше изображение: {width}x{height} пикселей.'
                    )

                # Проверка максимальных размеров
                if width > MAX_IMAGE_WIDTH or height > MAX_IMAGE_HEIGHT:
                    raise ValidationError(
                        f'Изображение слишком большое. '
                        f'Максимальные размеры: {MAX_IMAGE_WIDTH}x{MAX_IMAGE_HEIGHT} пикселей. '
                        f'Ваше изображение: {width}x{height} пикселей.'
                    )

                # Проверка соотношения сторон (опционально, можно убрать)
                aspect_ratio = width / height
                if aspect_ratio < 0.5 or aspect_ratio > 2.0:
                    raise ValidationError(
                        'Соотношение сторон изображения должно быть между 1:2 и 2:1. '
                        f'Текущее соотношение: {width}:{height}.'
                    )

        except Exception as e:
            raise ValidationError(
                'Не удалось прочитать размеры изображения. '
                'Пожалуйста, убедитесь, что файл является корректным изображением.'
            )

        # Проверка имени файла на запрещенные символы
        if not self._is_safe_filename(image.name):
            raise ValidationError(
                'Имя файла содержит недопустимые символы. '
                'Пожалуйста, переименуйте файл, используя только латинские буквы, '
                'цифры, дефис и подчеркивание.'
            )

        return image