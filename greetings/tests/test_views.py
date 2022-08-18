from django.test import TestCase, Client
from greetings.views import name


class MathViewsTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_greetings_main_page(self):
        response = self.client.get('/greetings/')
        self.assertIn('Hello World!', response.content.decode())

   