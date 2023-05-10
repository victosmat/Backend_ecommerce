from django.urls import path
from . import views

urlpatterns = [
    path('create_brand/', views.create_brand, name='create_brand'),
    path('create_shoe/', views.create_shoe, name='create_shoe'),
    path('delete_brand/<int:brand_id>/', views.delete_brand, name='delete_brand'),
    path('delete_shoe/<int:shoe_id>/', views.delete_shoe, name='delete_shoe'),
    path('search_brand/', views.search_brand, name='search_brand'),
    path('search_shoe/', views.search_shoe, name='search_shoe'),
]
