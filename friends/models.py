from django.db import models
from authentication.models import User
from constants import FriendStatus


class Friend(models.Model):
    """Model to store friend requests, and the relationship between two users"""

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User,
        related_name="friends",
        on_delete=models.CASCADE,
        null=True,
        blank=False,
    )
    friend = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=False,
    )
    status = models.CharField(
        max_length=20,
        choices=FriendStatus.choices,
        default=FriendStatus.REQUESTED,
    )
    is_sender = models.BooleanField(default=False)
    message = models.CharField(max_length=200, null=True, blank=True)
