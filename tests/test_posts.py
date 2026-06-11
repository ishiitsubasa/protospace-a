from django.test import TestCase
from django.urls import reverse
from tests.factories.posts import PostFactory

class PostIndexViewTest(TestCase):

    def setUp(self):
        self.post = PostFactory.build()

    def test_index_status_code(self):
        response = self.client.get(reverse('Posts:index'))
        self.assertEqual(response.status_code, 200)

    def test_index_template(self):
        response = self.client.get(reverse('Posts:index'))
        self.assertTemplateUsed(response, 'posts/index.html')

    def test_index_contains_post(self):
        response = self.client.get(reverse('Posts:index'))
        self.assertContains(response, self.post.name)