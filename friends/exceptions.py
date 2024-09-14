# This would contain all of the exceptions related to the friends app.


class FriendAlreadyExists(Exception):
    code = "user_friend_record_exists"
    detail = "User-friend record exists"
