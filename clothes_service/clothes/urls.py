from django.urls import path
from . import views

urlpatterns = [
    path('create_brand/', views.create_brand, name='create_brand'),
    path('create_clothing/', views.create_clothing, name='create_clothing'),
    path('delete_brand/<int:brand_id>/', views.delete_brand, name='delete_brand'),
    path('delete_clothing/<int:clothing_id>/', views.delete_clothing, name='delete_clothing'),
    path('search_brand/', views.search_brand, name='search_brand'),
    path('search_clothing/', views.search_clothing, name='search_clothing'),
]
