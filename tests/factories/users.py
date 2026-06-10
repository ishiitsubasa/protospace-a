import factory
import faker
from django.contrib.auth import get_user_model

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = factory.Faker('email')
    password = factory.Faker('password')
    nickname = factory.LazyAttribute(lambda obj: faker.Faker().first_name()[:10])
    profile = factory.LazyAttribute(lambda obj: faker.Faker().text()[:100])
    belonging = factory.LazyAttribute(lambda obj: faker.Faker().company()[:50])
    role = factory.LazyAttribute(lambda obj: faker.Faker().job()[:50])