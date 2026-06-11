from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from posts.models import Post
from comments.models import Comment

User = get_user_model()

class BaseCommentTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='user@example.com',
            nickname='user',
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
            user=self.user
        )
        self.comment_url = reverse('comments:create', kwargs={'pk': self.post.pk})
        self.detail_url = reverse('Posts:detail', kwargs={'pk': self.post.pk})

class CommentCreateSuccessTestCase(BaseCommentTestCase):

    # コメントがDBに保存される
    def test_comment_saved_to_db(self):
        self.client.login(email='user@example.com', password='password123')
        self.client.post(self.comment_url, {'text': 'テストコメント'})
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().text, 'テストコメント')

    # 投稿成功後に詳細ページへ遷移
    def test_redirect_to_detail_after_comment(self):
        self.client.login(email='user@example.com', password='password123')
        response = self.client.post(self.comment_url, {'text': 'テストコメント'})
        self.assertRedirects(response, self.detail_url)

    # 詳細ページにコメントと投稿者名が表示される
    def test_comment_displayed_on_detail(self):
        self.client.login(email='user@example.com', password='password123')
        self.client.post(self.comment_url, {'text': 'テストコメント'})
        response = self.client.get(self.detail_url)
        self.assertContains(response, 'テストコメント')
        self.assertContains(response, self.user.nickname)

    # 他の投稿の詳細ページにはコメントが表示されない
    def test_comment_not_displayed_on_other_detail(self):
        self.client.login(email='user@example.com', password='password123')
        self.client.post(self.comment_url, {'text': 'テストコメント'})
        other_post = Post.objects.create(
            name='別のアプリ',
            catchphrase='別のキャッチコピー',
            concept='別のコンセプト',
            image=SimpleUploadedFile('test2.jpg', b'\x47\x49\x46\x38\x39\x61', content_type='image/jpeg'),
            user=self.user
        )
        response = self.client.get(reverse('Posts:detail', kwargs={'pk': other_post.pk}))
        self.assertNotContains(response, 'テストコメント')

class CommentFormDisplayTestCase(BaseCommentTestCase):

    # ログイン済みにはフォームが表示される
    def test_form_displayed_when_logged_in(self):
        self.client.login(email='user@example.com', password='password123')
        response = self.client.get(self.detail_url)
        self.assertContains(response, '送信する')

    # 未ログインにはフォームが表示されない
    def test_form_not_displayed_when_logged_out(self):
        response = self.client.get(self.detail_url)
        self.assertNotContains(response, '送信する')

class CommentValidationTestCase(BaseCommentTestCase):

    # 空のコメントは投稿できない
    def test_empty_comment_not_saved(self):
        self.client.login(email='user@example.com', password='password123')
        response = self.client.post(self.comment_url, {'text': ''})
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(response.status_code, 200)

class CommentCascadeDeleteTestCase(BaseCommentTestCase):

    # 投稿削除時にコメントも削除される
    def test_comment_deleted_when_post_deleted(self):
        Comment.objects.create(
            text='テストコメント',
            user=self.user,
            post=self.post
        )
        self.assertEqual(Comment.objects.count(), 1)
        self.post.delete()
        self.assertEqual(Comment.objects.count(), 0)