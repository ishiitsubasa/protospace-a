import factory
from django.contrib.auth import get_user_model
from posts.models import Post
from django.core.files.uploadedfile import SimpleUploadedFile
from tests.factories.users import UserFactory

User = get_user_model()

class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    name = factory.Faker('word')
    catchphrase = factory.Faker('sentence')
    concept = factory.Faker('paragraph')
    image = factory.LazyAttribute(lambda _: SimpleUploadedFile(
        name='test_image.jpg',
        content=b'',
        content_type='image/jpeg'
    ))
    user = factory.SubFactory(UserFactory)