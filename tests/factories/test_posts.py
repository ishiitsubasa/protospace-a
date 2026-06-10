import factory
from factory.django import DjangoModelFactory
from faker import Faker
from tests.factories.users import UserFactory

from posts.models import Post

fake = Faker("ja_JP")  # 日本語データを生成


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    name = factory.LazyAttribute(lambda obj: fake.company())          # 会社名で代用
    catchphrase = factory.LazyAttribute(lambda obj: fake.catch_phrase())
    concept = factory.LazyAttribute(lambda obj: fake.text(max_nb_chars=200))
    image = factory.django.ImageField(filename="test.png")            # ダミー画像を自動生成
    user = factory.SubFactory(UserFactory)                            # Userも一緒に生成
    # created_at / updated_at は auto_now_add / auto_now なので指定不要






