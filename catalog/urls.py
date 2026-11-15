from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import (HomeView, Contacts, ProductListView, ProductDetailView, ProductCreateView,
                           ProductDeleteView, ProductUpdateView)


app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),                       # /catalog/
    path('contacts/', Contacts.as_view(), name='contacts'),          # /catalog/contacts/
    path('products/', ProductListView.as_view(), name='product_list'),  # /catalog/products/
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/add/', ProductCreateView.as_view(), name='product_add'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
]
