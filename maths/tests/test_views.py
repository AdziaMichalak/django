from django.test import TestCase, Client
from maths.models import Math


class MathViewsTest(TestCase):

    def setUp(self):
        Math.objects.create(operation='sub', a=20, b=30)
        self.client = Client()

    def test_maths_main_page(self):
        response = self.client.get('/maths/')
        self.assertIn('Tu będzie matma', response.content.decode())

    def test_maths_list(self):
        response = self.client.get('/maths/histories/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['maths']), 1)
        self.assertIn('<li><a href="/maths/histories/1">id:1, a=20, b=30, op=sub</a></li>', response.content.decode())

    def test_maths_details(self):
        response = self.client.get('/maths/histories/1')
        self.assertIn('<a href="/maths/histories/">back</a>', response.content.decode())

    def test_maths_add_as_example(self):
        response = self.client.get('/maths/add/1/2')
        self.assertIn('Wynik operacji 1 + 2 wynosi 3', response.content.decode())


class MathViewsPaginationTest(TestCase):
    fixtures = ['math', 'result']

    def setUp(self):
        self.client = Client()

    def test_get_first_5(self):
        response = self.client.get("/maths/histories/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["maths"]), 8)

    def test_get_last_page(self):
        response = self.client.get("/maths/histories/?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["maths"]), 8)