from django.shortcuts import get_object_or_404
from posts.models import Group, Post
from rest_framework import filters, mixins, permissions, viewsets
from django.core.exceptions import PermissionDenied

from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для объектов модели Post."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsAuthorOrReadOnly)
    ordering = ("-pub_date",)

    def perform_create(self, serializer):
        """Создает запись, где автором является текущий пользователь."""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("Изменение чужого поста запрещено!")
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("Удаление чужого поста запрещено!")
        super().perform_destroy(instance)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для объектов модели Group."""
    permission_classes = [permissions.IsAuthenticated]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для объектов модели Comment."""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]  # Изменено!

    def _get_post(self):
        """Возвращает объект текущей записи."""
        return get_object_or_404(Post, pk=self.kwargs.get("post_id"))

    def get_queryset(self):
        """Возвращает queryset с комментариями для текущей записи."""
        return self._get_post().comments.all()

    def perform_create(self, serializer):
        """Создает комментарий для текущего поста."""
        serializer.save(
            author=self.request.user,
            post=self._get_post()
        )

    def perform_update(self, serializer):
        """Проверяет права на изменение комментария."""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("Изменение чужого комментария запрещено!")
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        """Проверяет права на удаление комментария."""
        if instance.author != self.request.user:
            raise PermissionDenied("Удаление чужого комментария запрещено!")
        super().perform_destroy(instance)


class FollowViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """Вьюсет для объектов модели Follow."""

    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("following__username", "user__username")

    def get_queryset(self):
        """Возвращает queryset с подписками для текущего пользователя."""
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        """Создает подписку, где подписчиком является текущий пользователь."""
        serializer.save(user=self.request.user)
