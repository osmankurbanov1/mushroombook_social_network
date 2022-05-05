from rest_framework import serializers
from profiles.models import MyUser


class UserSerializer(serializers.ModelSerializer):
    """
    Serializing all Users
    """
    #  avatar = serializers.ImageField(read_only=True)

    class Meta:
        model = MyUser
        exclude = (
            "email",
            "phone",
            "password",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions"
        )
