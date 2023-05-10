from django.urls import path
from . import views

urlpatterns = [
    path('create_account/', views.create_account, name='create_account'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('create_fullname/', views.create_fullname, name='create_fullname'),
    path('create_address/', views.create_address, name='create_address'),
    path('create_customer/', views.create_customer, name='create_customer'),
    path('delete_customer/', views.delete_customer, name='delete_customer'),
]
