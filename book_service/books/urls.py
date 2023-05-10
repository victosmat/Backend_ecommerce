from django.urls import path
from . import views

urlpatterns = [
    path('authors/create/', views.create_author, name='create_author'),
    path('categories/create/', views.create_category, name='create_category'),
    path('books/create/', views.create_book, name='create_book'),
    path('books/<int:book_id>/delete/', views.delete_book, name='delete_book'),
    path('authors/search/', views.author_search, name='author_search'),
    path('categories/search/', views.category_search, name='category_search'),
    path('books/search/', views.book_search, name='book_search'),
]
