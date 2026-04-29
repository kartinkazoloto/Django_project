from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import HomeView, Contacts, ProductListView, ProductDetailView

app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', Contacts.as_view(), name='contacts'),
    path('product_list/', ProductListView.as_view(), name='product_list'),
    path('product_detail/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
]
