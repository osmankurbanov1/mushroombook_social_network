from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    """custom User model"""
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]
    bio = models.TextField(blank=True, null=True)
    user_photo = models.ImageField(upload_to='media/MEDIA_USER_IMAGE_DIR/avatar/', blank=True, null=True)
    user_gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=MALE)
    first_login = models.DateTimeField(null=True)
