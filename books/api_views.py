from rest_framework.viewsets import ModelViewSet

from books.models import Author
from books.serializers import AuthorSerializer

class AuthorViewset(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer