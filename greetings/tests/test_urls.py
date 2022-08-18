from unittest import TestCase
from django.urls import resolve
from greetings.views import helloWorld, helloWorldName


class TestUrls(TestCase):
    def test_resolution_main_page(self):
        resolver = resolve('/greetings/')
        self.assertEqual(resolver.func, helloWorld)

    def test_resolution_name(self):
        resolver = resolve('/greetings/test')
        self.assertEqual(resolver.func, helloWorldName)