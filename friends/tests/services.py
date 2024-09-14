# This would contain all of the test cases for the services in friends app.
# Depending on the number of services, this may be replaced with a folder
# containing a file for each service class e.g. friends/tests/services/ServiceClassName.py

# The tests for the services would be the most comprehensive and granular,
# as they would test the business logic of the application.
# The tests would cover the methods and properties of the service classes in isolation.
from django.test import TestCase
from friends.models import Friend
from friends.services import FriendRequestService
from friends.factories import FriendFactory
from authentication.factories import UserFactory
from constants import FriendStatus


class FriendRequestServiceTestCase(TestCase):
    """Test cases for the FriendRequestService class"""

    def setUp(self):
        self.user = UserFactory()
        self.friend = UserFactory()
        self.friend_request_service = FriendRequestService()

    def test_create_friend_request_creates_friend_records_correctly(self):
        self.assertFalse(
            Friend.objects.filter(user=self.user, friend=self.friend).exists()
        )
        self.friend_request_service.create_friend_request(
            self.user, self.friend, "Hello"
        )
        # User to friend
        friend_request_record_for_user = Friend.objects.get(
            user=self.user, friend=self.friend
        )
        self.assertEqual(friend_request_record_for_user.user, self.user)
        self.assertEqual(friend_request_record_for_user.friend, self.friend)
        self.assertEqual(friend_request_record_for_user.is_sender, True)
        self.assertEqual(friend_request_record_for_user.status, FriendStatus.REQUESTED)
        self.assertEqual(friend_request_record_for_user.message, None)
        # Friend to user
        friend_request_record_for_friend = Friend.objects.get(
            user=self.friend, friend=self.user
        )
        self.assertEqual(friend_request_record_for_friend.user, self.friend)
        self.assertEqual(friend_request_record_for_friend.friend, self.user)
        self.assertEqual(friend_request_record_for_friend.is_sender, False)
        self.assertEqual(friend_request_record_for_friend.message, "Hello")
        self.assertEqual(
            friend_request_record_for_friend.status, FriendStatus.REQUESTED
        )

    def test_get_user_and_friend_returns_correct_objects(self):
        user, friend = self.friend_request_service.get_user_and_friend(
            self.user.id, self.friend.id
        )
        self.assertEqual(user, self.user)
        self.assertEqual(friend, self.friend)

    def test_get_user_and_friend_with_invalid_user_id_throws_exception(self):
        with self.assertRaises(Exception) as context:
            self.friend_request_service.get_user_and_friend(100, self.friend.id)
            self.assertTrue(
                "User matching query does not exist" in str(context.exception)
            )

    def test_get_user_and_friend_with_invalid_friend_id_throws_exception(self):
        with self.assertRaises(Exception) as context:
            self.friend_request_service.get_user_and_friend(self.user.id, 100)
            self.assertTrue(
                "User matching query does not exist" in str(context.exception)
            )

    def test_check_if_friend_request_exists_returns_correctly(self):
        FriendFactory(user=self.user, friend=self.friend, is_sender=True)
        self.assertTrue(
            self.friend_request_service.check_if_friend_request_exists(
                self.user, self.friend
            )
        )
        self.assertTrue(
            self.friend_request_service.check_if_friend_request_exists(
                self.friend, self.user
            )
        )
