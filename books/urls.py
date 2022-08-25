from django.contrib import admin
from django.urls import path
from books import views
from books.views import (
    HomeListView,
    AuthorIndex,
    AuthorCreate,
    AuthorUpdate,
    AuthorDelete,
    HomeListView,
    BookIndex,
    BookCreate,
    BookUpdate,
    BookDelete,  
    CategoryBookListView, 
    contact_form, 
    login_to_comment_redirect, 
    rate_book,
    confirm_rent,
    return_book,
    rent_book,
    SearchBookListView)



urlpatterns = [
    path('index', views.IndexView.as_view(), name='index'),
    path('', HomeListView.as_view(), name='home'),
    path('authors/', AuthorIndex.as_view(), name='author_index'),
    path('authors/add', AuthorCreate.as_view(), name='author_create'),
    path('authors/<int:pk>', AuthorUpdate.as_view(), name='author_update'),
    path('authors/<int:pk>/delete', AuthorDelete.as_view(), name='author_delete'),
    path('books/', BookIndex.as_view(), name='book_index'),
    path('books/add', BookCreate.as_view(), name='book_create'),
    path('books/<int:pk>', BookUpdate.as_view(), name='book_update'),
    path('books/<int:pk>/delete', BookDelete.as_view(), name='book_delete'),
    path('books/<int:pk>/<rating>', rate_book, name='rate_book'),
    path('books/return-book/<int:pk>', return_book, name='return_book'),
    path('book/rent-book/<int:pk>', rent_book, name='rent_book'),
    path('confirm-rent-a-book/<int:pk>', confirm_rent, name="confirm_rent_view"),
    path('users/', views.UserIndex.as_view(), name='user_index'),
    path('users/add', views.UserCreate.as_view(), name='user_create'),
    path('users/<int:pk>', views.UserUpdate.as_view(), name='user_update'),
    path('users/<int:pk>/delete', views.UserDelete.as_view(), name='user_delete'),
    path('borrowbook/', views.LendBookCreate.as_view(), name='lendbook_create'),
    path('borrowbook/<int:pk>', views.LendBookUpdate.as_view(), name='lendbook_update'),
    path('contact/', contact_form, name='contact'),
    path('redirect-to-detail/<int:pk>', login_to_comment_redirect, name='login_to_comment_redirect'),
    path('category/<int:pk>', CategoryBookListView.as_view(), name='category'),
    path('search/', SearchBookListView.as_view(), name='search'),
    
]