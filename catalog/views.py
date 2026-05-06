from gettext import Catalog

from django.views.generic import TemplateView, ListView, DetailView
from catalog.models import Product


class HomeView(TemplateView):
    model = Product
    template_name = 'catalog/home_view.html'


class Contacts(TemplateView):
    model = Product
    template_name = 'catalog/contacts.html'


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product

# def home(request):
#     """Контроллер домашней страницы"""
#     products = Product.objects.all()
#     context = {'products': products,}
#     return render(request, 'home.html', context=context)

# def contacts(request):
#     if request.method == 'POST':
#         # Получение данных из формы
#         name = request.POST.get('name')
#         phone = request.POST.get('phone')
#         message = request.POST.get('message')
#
#         return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
#     return render(request, 'contacts.html')

# def products_list(request):
#     """Контроллер списка продуктов"""
#     products = Product.objects.all()
#     context = {'products': products,}
#     return render(request, 'products_list.html', context=context)

# def product_detail(request, product_id):
#     """Контроллер отдельного продукта"""
#     product = get_object_or_404(Product, id=product_id)
#     context = {'product': product}
#     return render(request, 'product_detail.html', context=context)
