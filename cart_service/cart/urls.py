from django.urls import path
from . import views

urlpatterns = [
    path('create_cart/', views.create_cart, name='create_cart'),
    path('add_item_to_cart/', views.add_item_to_cart, name='add_item_to_cart'),
    path('remove_item_from_cart/', views.remove_item_from_cart,
         name='remove_item_from_cart'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('show_cart/', views.show_cart, name='show_cart'),
    path("cart_reg_update/", views.cart_reg_update, name="cart_reg_update"),
]
