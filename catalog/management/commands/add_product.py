from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Product, Category

# class Command(BaseCommand):
#     help = 'Add test products to the database'
#
#     def handle(self, *args, **kwargs):
#         # Удаляем существующие записи
#         Product.objects.all().delete()
#         Category.objects.all().delete()
#
#         group, _ = Category.objects.get_or_create(name='Категория 7')
#
#         products = [
#             {'name': 'картофель', 'description': 'картофель молодой', 'category': Category},
#             {'name': 'морковь', 'description': 'морковь', 'category': Category},
#             {'name': 'огурец', 'description': 'огурец', 'category': Category},
#         ]
#
#         for product_data in products:
#             product, created = Product.objects.get_or_create(**product_data)
#             if created:
#                 self.stdout.write(self.style.SUCCESS(f'Successfully added product: {product.name}'))
#             else:
#                 self.stdout.write(self.style.WARNING(f'Product already exists: {product.name}'))


class Command(BaseCommand):
    help = 'Load test data from fixture'

    def handle(self, *args, **kwargs):
        # Удаляем существующие записи
        Product.objects.all().delete()
        Category.objects.all().delete()

        call_command('loaddata', 'category_fixture.json')
        self.stdout.write(self.style.SUCCESS('Successfully loaded data from fixture'))

        call_command('loaddata', 'product_fixture.json')
        self.stdout.write(self.style.SUCCESS('Successfully loaded data from fixture'))
