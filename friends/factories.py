import factory
from friends.models import Friend
from authentication.factories import UserFactory


class FriendFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Friend

    user = factory.SubFactory(UserFactory)
    friend = factory.SubFactory(UserFactory)
    status = "accepted"
    is_sender = False
    message = "hello"
