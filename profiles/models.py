from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class MyUser(AbstractUser):
    """custom user model"""
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]
    first_login = models.DateTimeField(null=True)
    phone = models.CharField(max_length=14)
    user_photo = models.ImageField(upload_to='media/MEDIA_USER_IMAGE_DIR/avatar/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=MALE)
