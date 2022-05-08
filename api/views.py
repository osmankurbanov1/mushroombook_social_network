from rest_framework.generics import (
    RetrieveUpdateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView,
    ListAPIView,
    )
from rest_framework import permissions, mixins, viewsets

from .serializers import UserSerializer, PostSerializer, CommentSerializer
from .permissions import IsProfileOwnerOrReadOnly, IsPostAuthorOrReadOnly, IsCommentAuthorOrReadOnly
from profiles.models import MyUser
from wall.models import Post, Comment


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
    View list of user`s Posts
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
