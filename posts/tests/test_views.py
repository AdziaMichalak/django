from django.test import TestCase, Client
from posts.models import Post, Author


class MathViewsTest(TestCase):

    def setUp(self):
        Author.objects.create(nick='Test123', email='test123@test123.pl', bio='Test123')
        self.a1 = Author.objects.get(nick='Test123')
        Post.objects.create(title='Test123', content='Test123', author_id=self.a1)

    def test_posts_main_page(self):
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('<b>To część stała szablonu głównego.</b>', response.content.decode())

    def test_posts_details(self):
        response = self.client.get('/posts/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('<td>Test123</td>', response.content.decode())

    def test_authors_main_page(self):
        response = self.client.get('/posts/authors')
        self.assertEqual(response.status_code, 200)
        self.assertIn('<li><a href="/posts/authors/1">Test123</a></li>', response.content.decode())

    def test_authors_details(self):
        response = self.client.get('/posts/authors/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('<td>test123@test123.pl</td>', response.content.decode())