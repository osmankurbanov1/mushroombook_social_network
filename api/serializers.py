from rest_framework import serializers

from profiles.models import MyUser
from wall.models import Post, Comment
from followers.models import Follower


class FollowerSerializer(serializers.ModelSerializer):
    """
    Serializing Followers
    """

    class Meta:
        model = Follower
        fields = ['id', 'user', 'follower_user']


class ListFollowerSerializer(serializers.ModelSerializer):
    """
    Serializing list of Followers
    """
    followers = FollowerSerializer(many=True, read_only=True)

    class Meta:
        model = Follower
        fields = ['followers']


class UserSerializer(serializers.ModelSerializer):
    """
    Serializing all Users
    """

    class Meta:
        model = MyUser
        fields = (
            "id", "username", "first_name", "last_name", "user_gender", "user_photo",
            "bio", "date_joined", "last_login", "first_login",
            )


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializing comments
    """

    comment_author = serializers.ReadOnlyField(source='user.username')
    is_deleted = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = ("id", "comment_author", "post", "text", "parent", "is_deleted")


class PostSerializer(serializers.ModelSerializer):
    """
    Serializing all Posts
    """

    post_author = serializers.ReadOnlyField(source='user.username')
    post_is_published = serializers.ReadOnlyField(default=True)
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = (
            "id", "post_created_date", "post_is_published",
            "post_author", "post_description", "list_of_mushrooms",
            "comments",
            )
