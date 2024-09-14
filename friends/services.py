# This would contain all of the services for the friends app.
# Depending on the number of services, this may be replaced with a folder
# containing a file for each model e.g. friends/services/ServiceClassName.py

# The services module is a collection of classes that contain the business logic for the application.
# Each class is a service that performs a specific task.
# The service classes are used by the views to perform the business logic.
# The service classes are also tested in the services test module, in isolation from the views and models.
# This allows for easier testing and maintenance of the services.
import logging
from typing import Tuple
from django.core.exceptions import ObjectDoesNotExist
from friends.models import Friend
from authentication.models import User

logger = logging.getLogger(__name__)


class FriendRequestService:
    """Service class for handling friend requests"""

    @staticmethod
    def create_friend_request(user: User, friend: Friend, message: str) -> None:
        """create a friend request record in the database for both user and friend pair"""
        try:
            Friend.objects.create(user=user, friend=friend, is_sender=True)
            Friend.objects.create(
                user=friend, friend=user, is_sender=False, message=message
            )
        except Exception as error:
            logging.error(
                f"create_friend_request failed for (user: {user.id}, friend: {friend.id}) - {error}",
            )
            raise Exception(
                f"create_friend_request failed for (user: {user.id}, friend: {friend.id})  - {error}"
            ) from error

    @staticmethod
    def get_user_and_friend(
        user_id: int,
        friend_id: int,
    ) -> Tuple[User, Friend]:
        """Fetch the user and friend object pair"""
        try:
            user = User.objects.get(id=user_id)
            friend = User.objects.get(id=friend_id)
        except User.DoesNotExist as error:
            logging.error(
                f"get_user_and_friend failed for (user: {user_id}, friend: {friend_id}) - {error}",
            )
            raise ObjectDoesNotExist(
                f"get_user_and_friend failed for (user: {user_id}, friend: {friend_id}) - {error}"
            ) from error
        else:
            return user, friend

    @staticmethod
    def check_if_friend_request_exists(user: User, friend: Friend) -> bool:
        """Check if a friend request record exists in the database"""

        if not user.id or not friend.id:
            # TODO throw exception
            pass

        if user.friends.filter(friend_id=friend.id).exists():
            return True
        if friend.friends.filter(friend_id=user.id).exists():
            return True

        return False
