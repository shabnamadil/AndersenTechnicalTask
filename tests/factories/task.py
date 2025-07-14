from django.contrib.auth import get_user_model

import factory

from apps.tasks.models import Task
from tests.helpers.test_helpers import generate_factory_content

from .user import UserFactory

User = get_user_model()


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    title = factory.LazyFunction(lambda: generate_factory_content())
    description = factory.Faker("sentence")
    user = factory.SubFactory(UserFactory)
