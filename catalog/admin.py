from django.contrib import admin
from .models import Product, Category
from blog.models import Record


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name', 'description',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description',)


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'description',
                    'image',
                    'is_published',)
    search_fields = ('name', 'description', 'is_published')
