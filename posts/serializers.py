from rest_framework import serializers

from posts.models import Post, Author, Tag

class PostSerializer(serializers.ModelSerializer):
   class Meta:
       model = Post
       fields = ('id', 'title', 'content', 'created', 'modified', 'author_id', 'image', 'tags')

class AuthorSerializer(serializers.ModelSerializer):
   class Meta:
       model = Author
       fields = ('id', 'nick', 'email')

class TagSerializer(serializers.ModelSerializer):
   class Meta:
       model = Tag
       fields = ('id', 'word', 'created')