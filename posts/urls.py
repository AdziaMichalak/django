from django.urls import path
from posts.views import posts_list, post_details, author_details, author_list

app_name = "posts"
urlpatterns = [
    path('', posts_list, name="list"),
    path('<int:id>', post_details, name="details"),
    path('authors', author_list, name="a_list"),
    path('authors/<int:id>', author_details, name="a_details"),
]