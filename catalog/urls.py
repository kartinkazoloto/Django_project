from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import (HomeView, Contacts, ProductListView, ProductDetailView, ProductCreateView,
                           ProductDeleteView, ProductUpdateView)


app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', Contacts.as_view(), name='contacts'),
    path('product_list/', ProductListView.as_view(), name='product_list'),
    path('product_detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/add/', ProductCreateView.as_view(), name='product_add'),
    path('product_detail/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit'),
    path('product_detail/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
]
