"""View функции приложения API."""
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from .permission import IsOwnerOrReadOnly
from posts.models import Post, Group
from .serializers import (
    PostSerializer,
    GroupSerializer,
    CommentSerializer,
    FollowSerializer
)
from .pagination import CustomPagination

FORBIDDDEN_403 = PermissionDenied("Изменение чужого контента запрещено!")


class PostViewSet(viewsets.ModelViewSet):
    """вью-сет для модели Post."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        IsOwnerOrReadOnly,
    )
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        """Переопределение автора на юзера."""
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """вью-сет для модели Group."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = None


class CommentViewSet(viewsets.ModelViewSet):
    """View комментариев."""

    serializer_class = CommentSerializer
    permission_classes = (
        IsOwnerOrReadOnly,
    )
    pagination_class = None

    def get_queryset(self):
        """Выборка комментариев."""
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        return post.comments.all()

    def perform_create(self, serializer):
        """Создание постов."""
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(viewsets.ModelViewSet):
    """вью-сет для модели Follow."""

    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.SearchFilter,)
    search_fields = ("following__username", "user__username")
    pagination_class = None

    def perfom_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.request.user.follower.all()
