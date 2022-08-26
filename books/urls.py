from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from books import views
from django.contrib.auth import views as auth_views

from .views import (
    BookDetailView,
    BooksListView,
    CategoryBookListView,
    confirm_rent_view,
    contact_form,
    HomeListView,
    login_to_comment_redirect,
    rate_book_view,
    return_book_view,
    rent_book_view,
    SearchBookListView,
)


urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('search-book-results/', SearchBookListView.as_view(), name='search'),
    path('authors/', views.AuthorIndex.as_view(), name='author_index'),
    path('authors/add', views.AuthorCreate.as_view(), name='author_create'),
    path('authors/<int:pk>', views.AuthorUpdate.as_view(), name='author_update'),
    path('authors/<int:pk>/delete', views.AuthorDelete.as_view(), name='author_delete'),
    #path('books/', views.BookIndex.as_view(), name='book_index'),
    #path('books/add', views.BookCreate.as_view(), name='book_create'),
    #path('books/<int:pk>', views.BookUpdate.as_view(), name='book_update'),
    #path('books/<int:pk>/delete', views.BookDelete.as_view(), name='book_delete'),
    path('books/', BooksListView.as_view(), name='books'),
    path('books/<int:pk>', BookDetailView.as_view(), name='bookDetail'),
    path('confirm-rent-a-book/<int:pk>', confirm_rent_view, name="confirm_rent"),
    path('books/rent-book/<int:pk>', rent_book_view, name='rent_book'),
    path('books/return-book/<int:pk>', return_book_view, name='return_book'),
    path('category/<int:pk>', CategoryBookListView.as_view(), name='category'),
    path('books/<int:pk>/<rating>', rate_book_view, name='rate_book'),
    path('contact/', contact_form, name='contact'),
    path('redirect-to-detail/<int:pk>', login_to_comment_redirect, name='login_to_comment_redirect'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('restartPassword/', auth_views.PasswordResetView.as_view(), name='resetPassword'),
    path('passwordResetDone/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('user/profile/', views.UserDetailView.as_view(), name='UserProfile'),
    path('user/profile/update', views.UserUpdateView.as_view(), name='UserUpdate'),
    path('user/profile/updateImage', views.ProfileUpdateView.as_view(), name='ProfileUpdate'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)