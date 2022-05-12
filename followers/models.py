from django.db import models
from django.conf import settings


class Follower(models.Model):
    """
    follower_user follows following_user
    """
    # Who follows - follower_user
    follower_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following',
        verbose_name='Who follows'
                                      )
    # To whom - following_user
    following_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followers",
        verbose_name='To whom'
    )

    objects = models.Manager()

    def __str__(self):
        return f'{self.follower_user} follows {self.following_user}'
