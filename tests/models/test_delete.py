from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Post

class PostDeleteTest(TestCase):
  def test_delete(self):
    user = get_user_model().objects.create_user('testuser')
    post = Post.objects.create(name='a', catchphrase='b', concept='c', user=user)
    self.client.post(f'/posts/{post.pk}/delete')
    self.assertEqual(Post.objects.count(), 0)
