from rest_framework import serializers
from rest_framework.fields import SerializerMethodField


from profiles.models import MyUser
from wall.models import Post, Comment, PostImage, PostLike
from followers.models import Follower


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ('user_liked', 'post')


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ('image', )


class FollowingSerializer(serializers.ModelSerializer):
    """
    Serializing Following users
    """

    class Meta:
        model = Follower
        fields = ('id', 'following_user')


class FollowerSerializer(serializers.ModelSerializer):
    """
    Serializing Followers
    """

    class Meta:
        model = Follower
        fields = ('id', 'follower_user')


class UserSerializer(serializers.ModelSerializer):
    """
    Serializing all Users
    """

    following = FollowingSerializer(read_only=True, many=True)
    followers = FollowerSerializer(read_only=True, many=True)

    class Meta:
        model = MyUser
        fields = (
            "id", "username", "first_name", "last_name", "user_gender", "user_photo",
            "bio", "date_joined", "last_login", "first_login", "following", "followers"
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
    images = PostImageSerializer(many=True, read_only=True)
    total_likes = SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id", "post_created_date", "post_is_published",
            "post_author", "post_description", "list_of_mushrooms",
            "comments", "images", "total_likes"
            )

    def get_total_likes(self, instance):
        return instance.likes.count()

    def create(self, validated_data):

        images_mv_dict = self.context.get('view').request.FILES
        request = self.context.get('request', None)
        post = Post.objects.create(post_description=validated_data.get('post_description'),
                                   post_author=request.user,
                                   list_of_mushrooms=validated_data.get('list_of_mushrooms'))

        for image_key in images_mv_dict.keys():
            for image in images_mv_dict.getlist(image_key):
                PostImage.objects.create(post=post, image=image)

        return post
