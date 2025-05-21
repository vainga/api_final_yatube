from django.contrib import admin

from .models import Comment, Follow, Group, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Класс настройки раздела записей."""

    list_display = (
        "pk",
        "text",
        "image",
        "pub_date",
        "author",
        "group",
        "count_comments",
    )
    empty_value_display = "-пусто-"
    list_editable = ("group",)
    list_filter = ("pub_date",)
    list_per_page = 10
    search_fields = ("text",)
    ordering = ("-pk",)

    @admin.display(description="Количество комментариев")
    def count_comments(self, obj):
        return obj.comments.count()

    count_comments.admin_order_field = "comments"


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Класс настройки раздела сообществ."""

    list_display = ("pk", "title", "slug", "description", "count_posts")
    empty_value_display = "-пусто-"
    list_filter = ("title",)
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-pk",)

    @admin.display(description="Количество записей")
    def count_posts(self, obj):
        return obj.posts.count()


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Класс настройки раздела комментариев."""

    list_display = ("pk", "post", "author", "text", "created")
    list_editable = ("author",)
    list_filter = ("author",)
    list_per_page = 10
    search_fields = ("text",)
    ordering = ("-pk",)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Класс настройки раздела подписок."""

    list_display = (
        "pk",
        "following",
        "user",
    )
    list_editable = ("following",)
    list_filter = ("following",)
    list_per_page = 10
    search_fields = ("following__username", "user__username")
    ordering = ("-pk",)


admin.site.site_title = "Администрирование Yatube"
admin.site.site_header = "Администрирование Yatube"
