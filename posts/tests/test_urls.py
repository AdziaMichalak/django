from unittest import TestCase
from django.urls import resolve
from posts.views import posts_list, post_details, author_details, author_list


class TestUrls(TestCase):

    def test_resolution_for_posts_list(self):
        resolver = resolve('/posts/')
        self.assertEqual(resolver.func, posts_list)

    def test_resolution_for_post_details(self):
        resolver = resolve('/posts/1')
        self.assertEqual(resolver.func, post_details)

    def test_resolution_for_author(self):
        resolver = resolve('/posts/authors')
        self.assertEqual(resolver.func, author_list)

    def test_resolution_for_author_details(self):
        resolver = resolve('/posts/authors/1')
        self.assertEqual(resolver.func, author_details)