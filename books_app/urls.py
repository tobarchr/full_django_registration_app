from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('register',views.register),
    path('login', views.login),
    path('books',views.books),
    path('books/<int:book_id>',views.book_details),
    path('add_book',views.add_book),
    path('delete_book/<int:book_id>',views.delete_book),
    path('update_book/<int:book_id>',views.update_book),
    path('log_off',views.log_off),
    path('add_favorite/<int:book_id>',views.add_to_favorite),
    path('remove_favorite/<int:book_id>',views.remove_favorite)
]