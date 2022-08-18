from unittest import TestCase
from django.urls import resolve
from greetings.views import greetings, name


class TestUrls(TestCase):
    def test_resolution_main_page(self):
        resolver = resolve('/greetings/')
        self.assertEqual(resolver.func, greetings)

    def test_resolution_name(self):
        resolver = resolve('/greetings/<name>/')
        self.assertEqual(resolver.func, name)