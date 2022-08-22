from django.contrib import admin
from posts.models import Post, Author, Tag


admin.site.register(Post)

admin.site.register(Author)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
   pass