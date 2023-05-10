from django.urls import path
from . import views

urlpatterns = [
    path('initiate/', views.initiate, name='initiate'),
    path('update_status/', views.update_status, name='update_status'),
    path('add_product/', views.add_product, name='add_product'),
    path('show_inventory/', views.show_inventory, name='show_inventory'),
    path('remove_product/', views.remove_product, name='remove_product'),
    path('check_availability/', views.check_availability, name='check_availability'),
]
