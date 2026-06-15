from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()

def make_image(filename="test.png"):
    return SimpleUploadedFile(
        filename,
        b"\x89PNG\r\n\x1a\n" + b"\x00" * 100,
        content_type="image/png",
    )

class BasePostCreateTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            nickname='テスト',
            password='password123',
            profile='プロフィール',
            belonging='所属',
            role='役割'
        )
        self.url = reverse('Posts:create')
        self.index_url = reverse('Posts:index')
        self.login_url = reverse('users:login')
        self.valid_data = {
            'name': 'テスト',
            'catchphrase': 'キャッチ',
            'concept': 'コンセプト',
        }

class PostCreateAccessTestCase(BasePostCreateTestCase):

    # ログイン済みは投稿ページにアクセスできる
    def test_logged_in_can_access_create(self):
        self.client.login(email='test@example.com', password='password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    # 未ログインはログインページへリダイレクト
    def test_not_logged_in_redirects_to_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{self.login_url}?next={self.url}')

class PostCreateSuccessTestCase(BasePostCreateTestCase):

    # 正常投稿でDBに保存される
    def test_post_saved_to_db(self):
        self.client.login(email='test@example.com', password='password123')
        before_count = Post.objects.count()
        self.client.post(self.url, {**self.valid_data, 'image': make_image()})
        self.assertEqual(Post.objects.count(), before_count + 1)

    # 正常投稿後にトップページへリダイレクト
    def test_redirect_to_index_after_post(self):
        self.client.login(email='test@example.com', password='password123')
        response = self.client.post(self.url, {**self.valid_data, 'image': make_image()})
        self.assertRedirects(response, self.index_url)

class PostCreateValidationTestCase(BasePostCreateTestCase):

    # nameが空だと投稿できない
    def test_name_required(self):
        self.client.login(email='test@example.com', password='password123')
        before_count = Post.objects.count()
        self.client.post(self.url, {**self.valid_data, 'name': '', 'image': make_image()})
        self.assertEqual(Post.objects.count(), before_count)

    # catchphraseが空だと投稿できない
    def test_catchphrase_required(self):
        self.client.login(email='test@example.com', password='password123')
        before_count = Post.objects.count()
        self.client.post(self.url, {**self.valid_data, 'catchphrase': '', 'image': make_image()})
        self.assertEqual(Post.objects.count(), before_count)

    # conceptが空だと投稿できない
    def test_concept_required(self):
        self.client.login(email='test@example.com', password='password123')
        before_count = Post.objects.count()
        self.client.post(self.url, {**self.valid_data, 'concept': '', 'image': make_image()})
        self.assertEqual(Post.objects.count(), before_count)

    # imageがないと投稿できない
    def test_image_required(self):
        self.client.login(email='test@example.com', password='password123')
        before_count = Post.objects.count()
        self.client.post(self.url, self.valid_data)
        self.assertEqual(Post.objects.count(), before_count)

    # バリデーションエラー時は同じページに留まる
    def test_stays_on_page_when_validation_fails(self):
        self.client.login(email='test@example.com', password='password123')
        response = self.client.post(self.url, {**self.valid_data, 'name': '', 'image': make_image()})
        self.assertEqual(response.status_code, 200)

    # バリデーションエラー時にcatchphraseが保持される
    def test_catchphrase_retained_on_error(self):
        self.client.login(email='test@example.com', password='password123')
        response = self.client.post(self.url, {**self.valid_data, 'name': '', 'image': make_image()})
        self.assertIn('キャッチ', response.context['form']['catchphrase'].value())

    # バリデーションエラー時にconceptが保持される
    def test_concept_retained_on_error(self):
        self.client.login(email='test@example.com', password='password123')
        response = self.client.post(self.url, {**self.valid_data, 'name': '', 'image': make_image()})
        self.assertIn('コンセプト', response.context['form']['concept'].value())