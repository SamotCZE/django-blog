from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory, Client
from django.core.urlresolvers import reverse
from django.utils import timezone
from model_mommy import mommy

from blog.views import post_list, post_new
from blog.models import Post


def add_middleware_to_request(request, middleware_class):
    middleware = middleware_class()
    middleware.process_request(request)
    return request


def add_middleware_to_response(request, middleware_class):
    middleware = middleware_class()
    middleware.process_request(request)


class BlogTest(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username='TestUser', email='email@email.com', password='testpass')
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        # Crete published post
        self.published_post = mommy.make(Post, published_date=timezone.now())
        # Crete not published post
        self.not_published_post = mommy.make(Post)
        self.client = Client()

    def test_post_list(self):
        request = self.factory.get(reverse('post_list'))

        with self.assertTemplateUsed(template_name='blog/post_list.html'):
            response = post_list(request)
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.published_post.title, response.content.decode())
            self.assertNotIn(self.not_published_post.title, response.content.decode())

    def test_post_detail(self):
        post = Post(author=self.user, title='Test title', text='Test text')
        post.save()
        response = self.client.get('/post/' + str(post.id) + "/", data={'pk': post.pk})
        self.assertTemplateUsed('blog/post_detail.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['post'], post)

    def test_new_post_get(self):
        request = self.factory.get(reverse('post_new'))
        request.user = self.user

        with self.assertTemplateUsed(template_name='blog/post_edit.html'):
            response = post_new(request)
            self.assertEqual(response.status_code, 200)

    def test_new_post_post(self):
        response = self.client.post('/post/new/', {'title': 'Test', 'text': 'Test'})
        self.assertEqual(response.status_code, 302)
