from django.urls import path
from . import views

urlpatterns = [
    path("add_cart/", views.get_cart, name = "add_cart"),
    path("cart_status/", views.cart_transaction_info, name = "cart_status"),
    path("cart_reg_update/", views.cart_reg_update, name = "cart_reg_update"),
]