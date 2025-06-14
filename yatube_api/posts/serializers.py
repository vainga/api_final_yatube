from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )
    image = serializers.ImageField(required=False)

    class Meta:
        fields = "__all__"
        model = Post
        read_only_fields = ("author", "pub_date")


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "post", "created")
        read_only_fields = ("author", "created", "post")


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all()
    )

    class Meta:
        fields = "__all__"
        model = Follow
        read_only_fields = ("user",)
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=["user", "following"],
                message="Вы уже подписаны на этого пользователя.",
            )
        ]

    def validate(self, data):
        if self.context["request"].user == data["following"]:
            raise serializers.ValidationError(
                "Нельзя подписаться на самого себя!"
            )
        return data
