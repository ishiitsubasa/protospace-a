from django.test import TestCase
from django.contrib.auth import get_user_model
from posts.models import Post
from django.urls import reverse

class PostDeleteTest(TestCase):
  def test_delete(self):
    user = get_user_model().objects.create_user('testuser',nickname='tesuto')
    post = Post.objects.create(name='a', catchphrase='b', concept='c', user=user)
    self.client.force_login(user)
    self.client.post(reverse('Posts:delete', kwargs={'pk': post.pk}))
    self.assertEqual(Post.objects.count(), 0)
    