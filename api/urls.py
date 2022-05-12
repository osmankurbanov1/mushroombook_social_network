from django.urls import path

from . import views


urlpatterns = [
    path('profiles/<int:pk>/', views.UserProfileView.as_view()),
    path('user-posts/<int:pk>/', views.PostListView.as_view()),
    path('posts/', views.PostView.as_view({'post': 'create'})),
    path('posts/<int:pk>/', views.PostView.as_view({
        'get': 'retrieve', 'put': 'update', 'delete': 'destroy'
    })),
    path('comments/', views.CommentListCreateView.as_view()),
    path('comments/<int:pk>/', views.CommentsView.as_view()),
    path('followers/<int:pk>/', views.FollowerView.as_view(
        {'post': 'create', 'delete': 'destroy'}
    )),
    path('feed/', views.FeedView.as_view()),
]
