from django.urls import path
from . import views

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('properties/<int:pk>/', views.property_detail, name='property_detail'),
    path('export-requests/', views.export_requests_csv, name='export_requests_csv'),
]
