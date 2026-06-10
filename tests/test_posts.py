from django.test import TestCase
from django.urls import reverse
from .models import Post
from django.contrib.auth import get_user_model

User = get_user_model()

class PostIndexViewTest(TestCase):

    def setUp(self):
        # テスト用ユーザーを作成
        self.user = User.objects.create_user(
            nickname='testuser',
            password='testpassword'
        )
        # テスト用の投稿を作成
        self.post = Post.objects.create(
            name='テスト投稿',
            catchphrase='テストキャッチコピー',
            concept='テストコンセプト',
            user=self.user
            # imageは任意なので省略OK
            # created_at, updated_atは自動で入るので省略OK
        )

    def test_index_status_code(self):
        # ページが200で返ってくるか
        response = self.client.get(reverse('Posts:index'))
        self.assertEqual(response.status_code, 200)

    def test_index_template(self):
        # 正しいテンプレートが使われているか
        response = self.client.get(reverse('Posts:index'))
        self.assertTemplateUsed(response, 'posts/index.html')

    def test_index_contains_post(self):
        # 投稿が一覧に表示されているか
        response = self.client.get(reverse('Posts:index'))
        self.assertContains(response, 'テスト投稿')