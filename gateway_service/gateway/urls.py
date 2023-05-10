from django.urls import path
from . import views
from .all_views import inventory_views, cart_views, order_views, user_views, products_views

urlpatterns = [

    # User
    path('register/', user_views.register, name='register'),

    # Products
    path('register_book/', products_views.register_book, name='register_book'),
    path('register_shoes/', products_views.register_shoes, name='register_shoes'),
    path('register_clothes/', products_views.register_clothes, name='register_clothes'),

    # Inventory
    path('inititate_inventory/', inventory_views.inititate_inventory, name='inititate_inventory'),
    path('add_product_to_inventory/', inventory_views.add_product_to_inventory, name='add_product_to_inventory'),
    path('remove_product_from_inventory/', inventory_views.remove_product_from_inventory, name='remove_product_from_inventory'),
    path('show_inventory/', inventory_views.show_inventory, name='show_inventory'),

    # Cart
    path('add_product_to_cart/', cart_views.add_product_to_cart, name='add_product_to_cart'),
    path('remove_item_from_cart/', cart_views.remove_item_from_cart, name='remove_item_from_cart'),
    path('show_cart/', cart_views.show_cart, name='show_cart'),
    path('purchase/', cart_views.purchase, name='purchase'),

    # Order
    path('track_order/', order_views.track_order, name='track_order'),
    path('update_order/', order_views.update_order, name='update_order'),
]