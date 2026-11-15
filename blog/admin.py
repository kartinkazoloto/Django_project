from django.contrib import admin
from blog.models import Record


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'description',
                    'image',
                    'is_published',)
    search_fields = ('name', 'description', 'is_published')
