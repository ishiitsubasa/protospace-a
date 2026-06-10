from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from posts.models import Post
from tests.factories.test_posts import PostFactory       # ① インポートパスを修正
from tests.factories.users import UserFactory

User = get_user_model()


def make_image(filename="test.png"):
    """テスト用ダミー画像を生成するヘルパー"""
    return SimpleUploadedFile(
        filename,
        b"\x89PNG\r\n\x1a\n" + b"\x00" * 100,
        content_type="image/png",
    )


class PostCreateViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.url = reverse("Posts:create")
        self.index_url = reverse("Posts:index")
        self.login_url = reverse("users:login")

        self.valid_data = {
            "name": "テストプロトタイプ",
            "catchphrase": "テストキャッチコピー",
            "concept": "テストコンセプト",
        }

    # ログインのヘルパー（② USERNAME_FIELD が email なので email でログイン）
    def login(self):
        self.client.login(email=self.user.email, password="password123")

    # ----------------------------------------------------------------
    # ログイン状態の場合のみ、投稿ページへ遷移できること
    # ----------------------------------------------------------------

    def test_ログイン済みユーザーは投稿ページにアクセスできる(self):
        self.login()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    # ----------------------------------------------------------------
    # ログアウト状態で投稿ページに遷移しようとすると、ログインページに遷移すること
    # ----------------------------------------------------------------

    def test_未ログインユーザーはログインページにリダイレクトされる(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{self.login_url}?next={self.url}")

    # ----------------------------------------------------------------
    # 必要な情報を適切に入力して「保存する」ボタンを押すと、
    # プロトタイプ情報がデータベースに保存されること
    # ----------------------------------------------------------------

    def test_正常な投稿でDBにレコードが作成される(self):
        self.login()
        before_count = Post.objects.count()

        self.client.post(self.url, {**self.valid_data, "image": make_image()})

        self.assertEqual(Post.objects.count(), before_count + 1)

    # ----------------------------------------------------------------
    # 正しく投稿できた場合は、トップページへ遷移すること
    # ----------------------------------------------------------------

    def test_正常投稿後にトップページへリダイレクトされる(self):
        self.login()

        response = self.client.post(
            self.url, {**self.valid_data, "image": make_image()}
        )

        self.assertRedirects(response, self.index_url)

    # ----------------------------------------------------------------
    # プロトタイプの名称が必須であること
    # ----------------------------------------------------------------

    def test_nameが空だと投稿できない(self):
        self.login()
        before_count = Post.objects.count()

        self.client.post(
            self.url, {**self.valid_data, "name": "", "image": make_image()}
        )

        self.assertEqual(Post.objects.count(), before_count)

    def test_nameが空だとフォームにエラーが表示される(self):
        self.login()

        response = self.client.post(
            self.url, {**self.valid_data, "name": "", "image": make_image()}
        )

        self.assertIn("name", response.context["form"].errors)

    # ----------------------------------------------------------------
    # キャッチコピーが必須であること
    # ----------------------------------------------------------------

    def test_catchphraseが空だと投稿できない(self):
        self.login()
        before_count = Post.objects.count()

        self.client.post(
            self.url, {**self.valid_data, "catchphrase": "", "image": make_image()}
        )

        self.assertEqual(Post.objects.count(), before_count)

    def test_catchphraseが空だとフォームにエラーが表示される(self):
        self.login()

        response = self.client.post(
            self.url, {**self.valid_data, "catchphrase": "", "image": make_image()}
        )

        self.assertIn("catchphrase", response.context["form"].errors)

    # ----------------------------------------------------------------
    # コンセプトの情報が必須であること
    # ----------------------------------------------------------------

    def test_conceptが空だと投稿できない(self):
        self.login()
        before_count = Post.objects.count()

        self.client.post(
            self.url, {**self.valid_data, "concept": "", "image": make_image()}
        )

        self.assertEqual(Post.objects.count(), before_count)

    def test_conceptが空だとフォームにエラーが表示される(self):
        self.login()

        response = self.client.post(
            self.url, {**self.valid_data, "concept": "", "image": make_image()}
        )

        self.assertIn("concept", response.context["form"].errors)

    # ----------------------------------------------------------------
    # 画像は1枚必須であること
    # ----------------------------------------------------------------

    def test_imageがないと投稿できない(self):
        self.login()
        before_count = Post.objects.count()

        self.client.post(self.url, self.valid_data)

        self.assertEqual(Post.objects.count(), before_count)

    def test_imageがないとフォームにエラーが表示される(self):
        self.login()

        response = self.client.post(self.url, self.valid_data)

        self.assertIn("image", response.context["form"].errors)

    # ----------------------------------------------------------------
    # 投稿に必要な情報が入力されていない場合は、投稿できずにそのページに留まること
    # ----------------------------------------------------------------

    def test_バリデーションエラー時は同じページに留まる(self):
        self.login()

        response = self.client.post(
            self.url, {**self.valid_data, "name": "", "image": make_image()}
        )

        self.assertEqual(response.status_code, 200)

    # ----------------------------------------------------------------
    # バリデーションエラー時でも入力済みの項目（画像以外）は消えないこと
    # ----------------------------------------------------------------

    def test_バリデーションエラー時にcatchphraseの入力値が保持される(self):
        self.login()

        response = self.client.post(
            self.url, {**self.valid_data, "name": "", "image": make_image()}
        )

        self.assertIn(
            "テストキャッチコピー",
            response.context["form"]["catchphrase"].value(),
        )

    def test_バリデーションエラー時にconceptの入力値が保持される(self):
        self.login()  # ③ nixkname のタイポを修正

        response = self.client.post(
            self.url, {**self.valid_data, "name": "", "image": make_image()}
        )

        self.assertIn(
            "テストコンセプト",
            response.context["form"]["concept"].value(),
        )
