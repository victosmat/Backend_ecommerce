from django.urls import path
from . import views

urlpatterns = [
    path('create_order/', views.create_order, name='create_order'),
    path('update_order/', views.update_order, name='update_order'),
    path('show_order/', views.show_order, name='show_order'),
]
