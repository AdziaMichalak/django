from django.test import TestCase
from posts.models import Post, Author
from posts.forms import PostForm, AuthorForm


class AuthorFormTest(TestCase):

    def DataBaseObjectsNumber(self):
        self.assertEqual(len(Author.objects.all()), 0)

    def DataBaseObjectsId(self, x):
        self.assertEqual(x.id, 1)

    def test_author_save_correct_data_value(self):
        data = {'nick': 'Test', 'email': 'test@test.pl', 'bio': 'TestoweBio'}
        self.DataBaseObjectsNumber()
        form = AuthorForm(data=data)
        self.assertTrue(form.is_valid())
        r = form.save()
        self.assertIsInstance(r, Author)
        self.DataBaseObjectsId(r)
        self.assertEqual(r.bio, 'TestoweBio')


class PostFormTest(TestCase):

    def setUp(self):
        Author.objects.create(nick='Test', email='test@test.pl', bio='Test')
        self.a1 = Author.objects.get(nick='Test')

    def DataBaseObjectsNumber(self):
        self.assertEqual(len(Post.objects.all()), 0)

    def DataBaseObjectsId(self, x):
        self.assertEqual(x.id, 1)

    def test_post_save_correct_data_value(self):
        data = {'title': 'Test111', 'content': 'Testowy content',
                'author_id': self.a1}
        self.DataBaseObjectsNumber()
        form = PostForm(data=data)
        self.assertTrue(form.is_valid())
        Post.objects.get_or_create(**form.cleaned_data)
        p = Post.objects.get(title=data['title'], content=data['content'], author_id=data['author_id'])
        self.assertIsInstance(p, Post)
        self.DataBaseObjectsId(p)
        self.assertEqual(p.content, 'Testowy content')