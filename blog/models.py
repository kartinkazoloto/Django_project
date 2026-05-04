from django.db import models

class Record(models.Model):
    name = models.CharField(max_length=150, verbose_name='заголовок')
    description = models.TextField(null=True, blank=True, verbose_name='содержимое')
    image = models.ImageField(upload_to='images/', verbose_name='превью', blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    is_published = models.BooleanField(default=False, verbose_name='признак публикации')
    number_of_views = models.PositiveIntegerField(default=0, verbose_name='количество просмотров')


    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'запись'
        verbose_name_plural = 'записи'