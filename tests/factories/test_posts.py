import factory
from factory.django import DjangoModelFactory
from faker import Faker
from django.contrib.auth import get_user_model

from posts.models import Post

fake = Faker("ja_JP")  # 日本語データを生成

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.Sequence(lambda n: f"user_{n}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "password123")


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    name = factory.LazyAttribute(lambda obj: fake.company())          # 会社名で代用
    catchphrase = factory.LazyAttribute(lambda obj: fake.catch_phrase())
    concept = factory.LazyAttribute(lambda obj: fake.text(max_nb_chars=200))
    image = factory.django.ImageField(filename="test.png")            # ダミー画像を自動生成
    user = factory.SubFactory(UserFactory)                            # Userも一緒に生成
    # created_at / updated_at は auto_now_add / auto_now なので指定不要






