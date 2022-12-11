"""Модуль сериализаторов для приложения api."""

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator


from posts.models import Comment, Post, User, Group, Follow


class UserSerializer(serializers.ModelSerializer):
    """Серилизатор user модели."""

    class Meta:
        """класс мета."""

        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
        )
        ref_name = "ReadOnlyUsers"


class PostSerializer(serializers.ModelSerializer):
    """Серилизатор постов."""

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        """класс мета."""

        model = Post
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    """Серилизатор групп."""

    class Meta:
        """класс мета."""

        model = Group
        fields = (
            "id",
            "title",
            "slug",
            "description",
        )


class CommentSerializer(serializers.ModelSerializer):
    """Серилизатор коментариев."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        """Клас мета."""

        fields = '__all__'
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор подписок."""

    user = serializers.SlugRelatedField(
        slug_field="username",
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(),
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field="username",
    )

    def validate_following(self, value):
        """Проверяем подписку на самого себя."""
        if value == self.context["request"].user:
            raise serializers.ValidationError(
                "Нельзя подписаться на самого себя."
            )
        return value

    class Meta:
        """Класс мета."""

        model = Follow
        fields = "__all__"

        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(), fields=("user", "following")
            )
        ]
