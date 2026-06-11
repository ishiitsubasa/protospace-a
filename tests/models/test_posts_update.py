from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from tests.factories.posts import PostFactory
from tests.factories.users import UserFactory


class UpdateViewTest(TestCase):

    def setUp(self):
        self.owner = UserFactory()
        self.other_user = UserFactory()
        self.post = PostFactory(user=self.owner)
        self.url = reverse('Posts:update', kwargs={'pk': self.post.pk})

    # アクセス権限

    def test_ログアウト状態で編集ページへアクセスするとログインページへリダイレクトされる(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')

    def test_ログイン状態で自分の投稿の編集ページへアクセスできる(self):
        self.client.force_login(self.owner)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_ログイン状態で他人の投稿の編集ページへアクセスするとトップページへリダイレクトされる(self):
        self.client.force_login(self.other_user)
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('Posts:index'))

    def test_ログイン状態で他人の投稿へPOSTしてもトップページへリダイレクトされる(self):
        self.client.force_login(self.other_user)
        response = self.client.post(self.url, {'name': '乗っ取り'})
        self.assertRedirects(response, reverse('Posts:index'))

    # 表示

    def test_編集ページのテンプレートはupdate_htmlが使われる(self):
        self.client.force_login(self.owner)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'posts/update.html')

    def test_編集ページを開いた時点で登録済みのname情報が表示される(self):
        self.client.force_login(self.owner)
        response = self.client.get(self.url)
        self.assertContains(response, self.post.name)

    def test_編集ページを開いた時点で登録済みのcatchphrase情報が表示される(self):
        self.client.force_login(self.owner)
        response = self.client.get(self.url)
        self.assertContains(response, self.post.catchphrase)

    # バリデーション

    def test_nameが空のまま保存するとページに留まる(self):
        self.client.force_login(self.owner)
        response = self.client.post(self.url, {
            'name': '',
            'catchphrase': 'キャッチコピー',
            'concept': 'コンセプト',
        })
        self.assertEqual(response.status_code, 200)

    def test_catchphraseが空のまま保存するとページに留まる(self):
        self.client.force_login(self.owner)
        response = self.client.post(self.url, {
            'name': 'プロトタイプ名',
            'catchphrase': '',
            'concept': 'コンセプト',
        })
        self.assertEqual(response.status_code, 200)

    def test_バリデーションエラー後もnameの入力値が消えない(self):
        self.client.force_login(self.owner)
        response = self.client.post(self.url, {
            'name': '入力済みの名前',
            'catchphrase': '',
            'concept': 'コンセプト',
        })
        self.assertContains(response, '入力済みの名前')

    def test_バリデーションエラー後もcatchphraseの入力値が消えない(self):
        self.client.force_login(self.owner)
        response = self.client.post(self.url, {
            'name': '',
            'catchphrase': '入力済みキャッチコピー',
            'concept': 'コンセプト',
        })
        self.assertContains(response, '入力済みキャッチコピー')

    # 正常更新

    def test_正しく編集するとプロトタイプ詳細ページへリダイレクトされる(self):
        self.client.force_login(self.owner)
        response = self.client.post(self.url, {
            'name': '新しいプロトタイプ名',
            'catchphrase': '新しいキャッチコピー',
            'concept': '新しいコンセプト',
        })
        self.assertRedirects(
            response,
            reverse('Posts:detail', kwargs={'pk': self.post.pk})
        )

    def test_正しく編集するとname_catchphrase_conceptがDBに保存される(self):
        self.client.force_login(self.owner)
        self.client.post(self.url, {
            'name': '更新後の名前',
            'catchphrase': '更新後のキャッチコピー',
            'concept': '更新後のコンセプト',
        })
        self.post.refresh_from_db()
        self.assertEqual(self.post.name, '更新後の名前')
        self.assertEqual(self.post.catchphrase, '更新後のキャッチコピー')
        self.assertEqual(self.post.concept, '更新後のコンセプト')

    # 画像処理

    def test_画像を送らずに保存しても既存画像が保持される(self):
        original_image_name = self.post.image.name

        self.client.force_login(self.owner)
        self.client.post(self.url, {
            'name': '更新後の名前',
            'catchphrase': '更新後のキャッチコピー',
            'concept': '更新後のコンセプト',
            # image フィールドは送らない
        })

        self.post.refresh_from_db()
        self.assertEqual(self.post.image.name, original_image_name)

    def test_新しい画像を送ると画像が差し替えられる(self):
        new_image = SimpleUploadedFile(
            name='new_image.jpg',
            content=b'new_image_bytes',
            content_type='image/jpeg',
        )

        self.client.force_login(self.owner)
        self.client.post(self.url, {
            'name': '更新後の名前',
            'catchphrase': '更新後のキャッチコピー',
            'concept': '更新後のコンセプト',
            'image': new_image,
        })

        self.post.refresh_from_db()
        self.assertIn('new_image', self.post.image.name)