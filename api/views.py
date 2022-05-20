from rest_framework.generics import (
    RetrieveUpdateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView,
    ListAPIView,
    )
from rest_framework import permissions, viewsets, response

from rest_framework.pagination import PageNumberPagination

from .serializers import (
    UserSerializer, PostSerializer, CommentSerializer,
    FollowingSerializer, PostLikeSerializer
)
from .permissions import IsProfileOwnerOrReadOnly, IsPostAuthorOrReadOnly, IsCommentAuthorOrReadOnly
from profiles.models import MyUser
from wall.models import Post, Comment, PostLike
from followers.models import Follower


class LikeCreateDestroyView(viewsets.ModelViewSet):
    """
    (Create) Like Post /
    (Destroy) Unlike Post
    """
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        try:
            post = Post.objects.get(id=kwargs['pk'])
        except Post.DoesNotExist:
            return response.Response(status=404)

        PostLike.objects.create(post=post, user_liked=request.user)
        return response.Response({'message': f'"{request.user} liked {post}"'}, status=201)

    def destroy(self, request, *args, **kwargs):
        try:
            like = PostLike.objects.get(post_id=kwargs['pk'], user_liked=request.user)
        except Follower.DoesNotExist:
            return response.Response(status=404)
        like.delete()
        return response.Response({'message': 'unliked'}, status=200)


class PostListFeedPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class FeedView(ListAPIView):
    """
    List of following users posts
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = PostSerializer
    pagination_class = PostListFeedPagination

    def get_queryset(self):
        return Post.objects.filter(post_author__followers__follower_user=self.request.user). \
            order_by('-post_created_date').prefetch_related('comments')


class FollowerView(viewsets.ModelViewSet):
    """
    (Create) Subscribe to the User /
    (Destroy) Unsubscribe from the User
    """
    queryset = Follower.objects.all()
    serializer_class = FollowingSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        try:
            user = MyUser.objects.get(id=kwargs['pk'])
        except Follower.DoesNotExist:
            return response.Response(status=404)
        Follower.objects.create(follower_user=request.user, following_user=user)
        return response.Response({'message': f'"{request.user} followed to {user}"'}, status=201)

    def destroy(self, request, *args, **kwargs):
        try:
            user = Follower.objects.get(follower_user=request.user, following_user_id=kwargs['pk'])
        except Follower.DoesNotExist:
            return response.Response(status=404)
        user.delete()
        return response.Response({'message': 'unfollowed'}, status=200)


class UserProfileView(RetrieveUpdateAPIView):
    """
    Get/update the User Profile
    """
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsProfileOwnerOrReadOnly, )


class PostView(viewsets.ModelViewSet):

    """
    CRUD operations for the Post
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsPostAuthorOrReadOnly, )


class PostListView(ListAPIView):
    """
    View list of user`s Posts by pk
    """

    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Post.objects.filter(post_author_id=self.kwargs.get('pk'))


class CommentsView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve/update/destroy the Comment
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsCommentAuthorOrReadOnly, )

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()


class CommentListCreateView(ListCreateAPIView):
    """
    Create a Comment / View list of comments
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(comment_author=self.request.user)
