# This would contain all of the views for the friends app.
# Depending on the number of views, this may be replaced with a folder
# containing a file for each model e.g. friends/views/ViewSet.py
# This would also contain the serializers for each individual ViewSet in the friends app.
# e.g InputSerialiser, OutputSerializer etc.

# The views implement very little logic, and are mostly used to call the services and return the response.
# The views are also responsible for handling the request and response objects.
# The views are tested in the views test module, and are only interested in the request and response objects.
# e.g. if a request object with a certain payload is passed, a certain response object is expected to be returned.
import logging
from knox.auth import TokenAuthentication
from rest_framework.views import APIView
from rest_framework import status, response, serializers
from friends.services import FriendRequestService
from friends.exceptions import FriendAlreadyExists


logger = logging.getLogger(__name__)


# This is labelled as Create to align with CRUD operations
# But is referred to as a friend request throughout the codebase
class FriendCreateApi(APIView):
    """Api to create a friend request record in the database for both user and friend pair"""

    authentication_classes = [TokenAuthentication]

    class InputSerializer(serializers.Serializer):
        user_id = serializers.IntegerField(required=False)
        friend_id = serializers.IntegerField()
        message = serializers.CharField()

    def post(self, request):
        friend_request_service = FriendRequestService()
        try:
            serializer = self.InputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_id = request.data.get("user_id", None)
            if not user_id:
                # if user is requesting for themself
                user_id = request.user.id

            friend_id = request.data.get("friend_id")
            message = request.data.get("message")

            # get user and friend object pair
            user, friend = friend_request_service.get_user_and_friend(
                user_id, friend_id
            )
            # check if friend (or friend request) record already exists
            if friend_request_service.check_if_friend_request_exists(user, friend):
                raise FriendAlreadyExists(
                    f"You are already friends - {user.id}, {friend.id}"
                )

            # create friend request record
            friend_request_service.create_friend_request(user, friend, message)

        except (serializers.ValidationError, FriendAlreadyExists) as error:
            logging.error(f"FriendCreateApi.post failed - {error}")
            return response.Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=[{"error": str(error)}],
            )
        # Catch all exception
        except Exception as error:
            logging.error(
                f"FriendCreateApi.post failed - {error}",
            )
            # This will raise exception message in format:
            # ViewName.method failed - ServiceFunction and details - Exception message
            # FriendCreateApi.post failed - get_user_and_friend failed for (user: 1, friend: 100)
            # - User matching query does not exist.
            raise Exception(f"FriendCreateApi.post failed - {error}") from error
        else:
            return response.Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
