"""View функции приложения API."""
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import mixins
from rest_framework import filters
from .permission import IsOwnerOrReadOnly
from posts.models import Post, Group, Comment, Follow
from .serializers import (
    PostSerializer,
    GroupSerializer,
    CommentSerializer,
    FollowSerializer
)

FORBIDDDEN_403 = PermissionDenied("Изменение чужого контента запрещено!")


class PostViewSet(viewsets.ModelViewSet):
    """вью-сет для модели Post."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        IsOwnerOrReadOnly,
    )
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Переопределение автора на юзера."""
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """вью-сет для модели Group."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = None


class CommentViewSet(viewsets.ModelViewSet):
    """вью-сет для модели Comment."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = None

    def get_queryset(self):
        """Выборка комментариев."""
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        return post.comments.all()

    def perform_create(self, serializer):
        """Переопределение автора на юзера."""
        serializer.save(author=self.request.user)


class FollowViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """вью-сет для модели Follow."""

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username', 'user__username')

    def get_queryset(self):
        """Возвращает отфильтрованный список подписок."""
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Переопределение автора на юзера."""
        serializer.save(user=self.request.user)
