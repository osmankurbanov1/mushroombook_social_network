from django.db import models
from django.conf import settings

from mptt.models import MPTTModel, TreeForeignKey

from comments.models import AbstractComment


class Post(models.Model):
    """
    Post model
    """

    SEASON_CHOICES = [
        ('Winter', 'Winter'),
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
        ('Autumn', 'Autumn'),
    ]

    post_description = models.TextField(max_length=1500)
    list_of_mushrooms = models.CharField(max_length=200, null=True)
    hunting_location = models.CharField(max_length=50, null=True)
    season_of_the_year = models.CharField(max_length=6, choices=SEASON_CHOICES, null=True)
    hunting_date = models.DateField(null=True)
    post_created_date = models.DateTimeField(auto_now_add=True)
    post_is_published = models.BooleanField(default=True)
    count_of_post_views = models.PositiveIntegerField(default=0)
    post_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return f'Post by {self.post_author} / created date: {self.post_created_date}'

    objects = models.Manager()


class Comment(AbstractComment, MPTTModel):
    """
    Comment to the post
    """
    comment_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    parent = TreeForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children'
    )

    def __str__(self):
        return f'{self.comment_author} - {self.post}'


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.FileField(upload_to='MEDIA_IMAGE_DIR/post_images/')

    def __str__(self):
        return f'Image(s) for {self.post}'
