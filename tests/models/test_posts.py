from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from posts.models import Post

User = get_user_model()

class BasePostDetailTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(
            email='owner@example.com',
            nickname='owner',
            password='password123',
            profile='プロフィール',
            belonging='所属',
            role='役割'
        )
        self.other_user = User.objects.create_user(
            email='other@example.com',
            nickname='other',
            password='password123',
            profile='プロフィール2',
            belonging='所属2',
            role='役割2'
        )
        self.image = SimpleUploadedFile(
            'test.jpg',
            b'\x47\x49\x46\x38\x39\x61',
            content_type='image/jpeg'
        )
        self.post = Post.objects.create(
            name='テストアプリ',
            catchphrase='キャッチコピー',
            concept='コンセプト',
            image=self.image,
            user=self.owner
        )
        self.detail_url = reverse('Posts:detail', kwargs={'pk': self.post.pk})

class PostDetailAccessTestCase(BasePostDetailTestCase):

    def test_not_logged_in_can_access_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)

    def test_logged_in_can_access_detail(self):
        self.client.login(email='owner@example.com', password='password123')
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)

    def test_index_has_link_to_detail(self):
        response = self.client.get(reverse('Posts:index'))
        self.assertContains(response, self.detail_url)

class PostDetailContentTestCase(BasePostDetailTestCase):

    def test_post_info_displayed(self):
        response = self.client.get(self.detail_url)
        self.assertContains(response, 'テストアプリ')
        self.assertContains(response, 'キャッチコピー')
        self.assertContains(response, 'コンセプト')
        self.assertContains(response, self.owner.nickname)

    def test_image_displayed(self):
        response = self.client.get(self.detail_url)
        self.assertContains(response, self.post.image.url)

class PostDetailButtonTestCase(BasePostDetailTestCase):

    def test_not_logged_in_no_buttons(self):
        response = self.client.get(self.detail_url)
        self.assertNotContains(response, '編集する')
        self.assertNotContains(response, '削除する')

    def test_owner_sees_buttons(self):
        self.client.login(email='owner@example.com', password='password123')
        response = self.client.get(self.detail_url)
        self.assertContains(response, '編集する')
        self.assertContains(response, '削除する')

    def test_other_user_no_buttons(self):
        self.client.login(email='other@example.com', password='password123')
        response = self.client.get(self.detail_url)
        self.assertNotContains(response, '編集する')
        self.assertNotContains(response, '削除する')