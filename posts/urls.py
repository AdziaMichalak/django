from django.urls import path
from django.views.generic import ListView
from posts.models import Post
from posts.views import posts_list, post_details, author_list, author_details


app_name = "posts"

urlpatterns = [
   path('', posts_list, name="list"),
   path('<int:id>', post_details, name="details"),
   path('authors', author_list, name="authors"),
   path('authors/<int:id>', author_details, name="author"),
   path('list', ListView.as_view(model=Post), name="posts_list")
]