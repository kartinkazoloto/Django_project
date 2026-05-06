"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from .apps import BlogConfig
from .views import CreateRecord, HomeView, RecordDetailView, RecordListView, RecordDeleteView, RecordUpdateView

app_name = BlogConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('create/', CreateRecord.as_view(), name='create'),
    path('blog_list/', RecordListView.as_view(), name='blog_list'),
    path('record_detail/<int:pk>/', RecordDetailView.as_view(), name='record_detail'),
    path('record_detail/<int:pk>/edit/', RecordUpdateView.as_view(), name='record_edit'),
    path('record_detail/<int:pk>/delete/', RecordDeleteView.as_view(), name='record_delete'),
]