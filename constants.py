# Contains all the constants used in the project
# constants are kept in one place to make it easier to maintain/extend them
# and to avoid constant duplication


class FriendStatus:
    REQUESTED = "requested"
    ACCEPTED = "accepted"
    BLOCKED = "blocked"

    choices = (
        (REQUESTED, "requested"),
        (ACCEPTED, "accepted"),
        (BLOCKED, "blocked"),
    )
