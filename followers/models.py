from django.db import models
from django.conf import settings


class Follower(models.Model):
    """
    Follower/Following user model
    """
    objects = models.Manager()

    # Who follows
    follower_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following',
        verbose_name='Who follows'
                                      )
    # To whom
    following_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followers",
        verbose_name='To whom'
    )

    def __str__(self):
        return f'{self.follower_user} follows {self.following_user}'

    class Meta:
        unique_together = (('follower_user', 'following_user'), )
