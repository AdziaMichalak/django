from rest_framework import routers
from posts import api_views as posts_views
from books import api_views as books_views

router = routers.DefaultRouter()
router.register('posts', posts_views.PostViewset)
router.register('books', books_views.AuthorViewset)