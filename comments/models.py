from django.db import models


class AbstractComment(models.Model):
    """
    Abstract comment model
    """
    text = models.TextField(max_length=400)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'Comment`s text: {self.text}'

    class Meta:
        abstract = True
