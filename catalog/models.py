from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
import os

class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='наименование')
    description = models.TextField(max_length=150, verbose_name='описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    """Модель товара"""
    name = models.CharField(max_length=150, verbose_name='наименование')
    description = models.TextField(null=True, blank=True, verbose_name='описание')
    image = models.ImageField(
        upload_to='images/',
        verbose_name='изображение',
        blank=True,
        null=True,
        help_text='Допустимые форматы: JPEG, PNG. Максимальный размер: 5 МБ.')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='products', verbose_name='Категория')
    price = models.PositiveIntegerField(default=0, verbose_name='Стоимость')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:product_detail', kwargs={'pk': self.pk})

    def clean(self):
        """Валидация на уровне модели"""
        if self.price < 0:
            raise ValidationError({'price': 'Цена не может быть отрицательной.'})

        # Валидация изображения на уровне модели
        if self.image:
            from django.core.files.images import get_image_dimensions

            # Проверка размера файла (5 МБ)
            if self.image.size > 5 * 1024 * 1024:
                raise ValidationError({
                    'image': 'Размер файла превышает 5 МБ.'
                })

            # Проверка расширения
            ext = os.path.splitext(self.image.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png']:
                raise ValidationError({
                    'image': 'Допустимые форматы: JPEG, PNG.'
                })

            # Проверка размеров изображения
            try:
                width, height = get_image_dimensions(self.image)
                if width and height:
                    if width < 100 or height < 100:
                        raise ValidationError({
                            'image': 'Изображение слишком маленькое. Минимальные размеры: 100x100 пикселей.'
                        })
            except:
                pass