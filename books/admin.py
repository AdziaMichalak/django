from django.contrib import admin

from .models import Author, Book, BookRentHistory, Category, InBoxMessages, BorrowBook, Profile
# Register your models here.


@admin.register(Author)
class Author(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name"]
    search_fields = ["name"]


@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ["id", "category"]


@admin.register(Book)
class Book(admin.ModelAdmin):
    list_display = ["id", "name", "author_id", "status", "category", "image", "last_rating", "created", "modified", "book_amount"]
    list_filter = ["name"]
    search_fields = ["name"]


@admin.register(BookRentHistory)
class BookRentHistoryAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'rent_date']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(InBoxMessages)
class InBoxMessagesAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'message']

admin.site.register(Profile)

@admin.register(BorrowBook)
class BorrowBook(admin.ModelAdmin):
    list_display = ["status", "library_user", "book", "lend_date", "return_date"]