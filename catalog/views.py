from django.contrib import messages
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, UpdateView
from catalog.models import Product
from .forms import ProductForm
from django.urls import reverse_lazy


class HomeView(TemplateView):
    model = Product
    template_name = 'catalog/home_view.html'


class Contacts(TemplateView):
    """Страница контактов"""
    model = Product
    template_name = 'catalog/contacts.html'


class ProductListView(ListView):
    """Список товаров"""
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 12


class ProductDetailView(DetailView):
    """Детальная страница товара"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'object'


class ProductCreateView(CreateView):
    """Создание нового товара"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_add.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        """Обработка успешного сохранения формы"""
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Товар "{form.instance.name}" успешно добавлен!'
        )
        return response

    def form_invalid(self, form):
        """Обработка ошибок формы"""
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'{error}')
        return super().form_invalid(form)


class ProductUpdateView(UpdateView):
    """Редактирование товара"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_edit.html'
    success_url = reverse_lazy('catalog:product_list')
    context_object_name = 'product'

    def form_valid(self, form):
        """Обработка успешного обновления"""
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Товар "{form.instance.name}" успешно обновлен!'
        )
        return response

    def form_invalid(self, form):
        """Обработка ошибок валидации"""
        # Правильная обработка ошибок формы
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'{error}')
        return super().form_invalid(form)

# Удаление товара (DELETE)
class ProductDeleteView(DeleteView):
    """Удаление товара"""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

    def delete(self, request, *args, **kwargs):
        """Обработка успешного удаления"""
        product = self.get_object()
        product_name = product.name
        response = super().delete(request, *args, **kwargs)
        messages.success(
            request,
            f'Товар "{product_name}" успешно удален!'
        )
        return response
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
