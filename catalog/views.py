from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, DeleteView, UpdateView
)
from django.urls import reverse_lazy

from catalog.models import Product
from .forms import ProductForm


class HomeView(TemplateView):
    """Главная страница"""
    template_name = 'catalog/home_view.html'


class Contacts(TemplateView):
    """Страница контактов"""
    template_name = 'catalog/contacts.html'


class ProductListView(ListView):
    """Список товаров — ОБЩЕДОСТУПЕН"""
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 12


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Детальная страница товара — только для авторизованных"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'object'


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание товара — только для авторизованных"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_add.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Товар "{form.instance.name}" успешно добавлен!'
        )
        return response

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'{error}')
        return super().form_invalid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование товара — только для авторизованных"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_edit.html'
    success_url = reverse_lazy('catalog:product_list')
    context_object_name = 'product'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Товар "{form.instance.name}" успешно обновлен!'
        )
        return response

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'{error}')
        return super().form_invalid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление товара — только для авторизованных"""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        product_name = product.name
        response = super().delete(request, *args, **kwargs)
        messages.success(
            request,
            f'Товар "{product_name}" успешно удален!'
        )
        return response