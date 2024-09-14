# This would contain all of the test cases for the views in friends app.
# Depending on the number of views, this may be replaced with a folder
# containing a file for each ViewSet e.g. friends/tests/views/ViewSetName.py

# The tests for the views would only be concerned with
# the request data and the response of the view and the data it returns
# e.g. the request object, data returned from the serializer, the status code of the response etc.
from rest_framework.test import APITestCase
from authentication.factories import UserFactory
from friends.factories import FriendFactory


class FriendCreateApiTestCase(APITestCase):
    """Test cases for creating a friend request using the FriendCreateApi view"""

    def setUp(self):
        self.user = UserFactory()
        self.friend = UserFactory()

    def test_create_friend_request_returns_200(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/friends/request/",
            {"friend_id": self.friend.id, "message": "Hello"},
        )
        self.assertEqual(response.status_code, 200)

    def test_create_friend_request_with_invalid_friend_returns_400(self):
        self.client.force_authenticate(user=self.user)

        with self.assertRaises(Exception) as context:
            response = self.client.post(
                "/api/friends/request/",
                {"friend_id": 100, "message": "Hello"},
            )
            self.assertEqual(response.status_code, 400)
            # Check that error context is passed correctly
            self.assertTrue("get_user_and_friend failed" in str(context.exception))

    def test_create_friend_request_with_invalid_user_returns_400(self):
        with self.assertRaises(Exception) as context:
            response = self.client.post(
                "/api/friends/request/",
                {"friend_id": self.friend.id, "message": "Hello"},
            )
            self.assertEqual(response.status_code, 400)
            # Check that error context is passed correctly
            self.assertTrue("get_user_and_friend failed" in str(context.exception))

    def test_create_friend_request_with_existing_friend_request_returns_400(self):
        FriendFactory(user=self.user, friend=self.friend, is_sender=True)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/friends/request/",
            {"friend_id": self.friend.id, "message": "Hello"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data,
            [{"error": f"You are already friends - {self.user.id}, {self.friend.id}"}],
        )
