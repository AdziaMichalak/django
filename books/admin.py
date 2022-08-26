from django.contrib import admin
from books.models import Author, Book, Category, BorrowBook, Profile

@admin.register(Author)
class Author(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name"]
    search_fields = ["name"]

@admin.register(Book)
class Book(admin.ModelAdmin):
    list_display = ["id", "name", "status", "category", "image", "last_rating", "created", "modified"]
    list_filter = ["authors"]
    search_fields = ["name"]


@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ["id", "category"]

admin.site.register(Profile)
admin.site.register(BorrowBook)
