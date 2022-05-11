from rest_framework.generics import (
    RetrieveUpdateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView,
    ListAPIView,
    )
from rest_framework import permissions, viewsets, response

from .serializers import (
    UserSerializer, PostSerializer, CommentSerializer,
    FollowerSerializer
)
from .permissions import IsProfileOwnerOrReadOnly, IsPostAuthorOrReadOnly, IsCommentAuthorOrReadOnly
from profiles.models import MyUser
from wall.models import Post, Comment
from followers.models import Follower


class ListFollowerView(ListAPIView):
    """
    Get the list of current user followers
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = FollowerSerializer

    def get_queryset(self):
        return Follower.objects.filter(user=self.request.user)


class FollowerView(viewsets.ModelViewSet):
    """
    (Create) Subscribe to the User /
    (Destroy) Unsubscribe from the User
    """
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        try:
            user = MyUser.objects.get(id=kwargs['pk'])
        except Follower.DoesNotExist:
            return response.Response({'message': 'no user with this pk'}, status=404)
        Follower.objects.create(follower_user=request.user, user=user)
        return response.Response({'message': 'now you are following'}, status=201)

    def destroy(self, request, *args, **kwargs):
        try:
            follower = Follower.objects.get(follower_user=request.user, user_id=kwargs['pk'])
        except Follower.DoesNotExist:
            return response.Response({'message': 'no user with this pk'}, status=404)
        follower.delete()
        return response.Response({'message': 'and now you unfollowing'}, status=204)


class UsersProfileView(RetrieveUpdateAPIView):
    """
    Get/update the User
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

    def perform_create(self, serializer):
        serializer.save(post_author=self.request.user)


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
