from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, ReplyView, ResolvedPostListView, UnresolvedPostListView, UnreadPostListView
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='posts-home'),  # leave blank for home, have specific naming for path
    path('user/posts', UserPostListView.as_view(), name='user-posts'),
    path('user/resolved-posts', ResolvedPostListView.as_view(), name='resolved-posts'),
    path('user/unresolved-posts', UnresolvedPostListView.as_view(), name='unresolved-posts'),
    path('user/unread-posts', UnreadPostListView.as_view(), name='unread-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/reply/', ReplyView.as_view(), name='reply-post'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
]