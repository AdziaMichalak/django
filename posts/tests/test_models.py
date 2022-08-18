from django.test import TestCase
from posts.models import Post, Author


class PostAuthorModelTest(TestCase):
    def setUp(self):
        Author.objects.create(nick='Test', email='test@test.pl', bio='Test')
        self.a1 = Author.objects.get(nick='Test')
        Post.objects.create(title='TestXX', content='Lala', author_id=self.a1)

    def test_author(self):
        self.assertEqual(str(self.a1), 'nick: Test, email: test@test.pl, bio: Test')

    def test_post(self):
        p1 = Post.objects.get(author_id=self.a1)

        self.assertEqual(str(p1.title), 'TestXX')
        self.assertEqual(str(p1.content), 'Lala')
        self.assertEqual(str(p1.author_id), 'nick: Test, email: test@test.pl, bio: Test')