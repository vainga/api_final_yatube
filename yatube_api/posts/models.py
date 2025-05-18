from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import Truncator

from posts.constants import TEXT_DISPLAY_LENGTH, WORDS_DISPLAY_LENGTH

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        'Заголовок',
        max_length=200,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )
    description = models.TextField('Описание',)

    class Meta:
        verbose_name = 'сообщество'
        verbose_name_plural = 'Сообщества'
        ordering = ['title', 'id']

    def __str__(self):
        return Truncator(self.title).words(WORDS_DISPLAY_LENGTH)


class Post(models.Model):
    text = models.TextField('Текст публикации')
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    image = models.ImageField(
        upload_to='posts/',
        null=True,
        blank=True,
        verbose_name='Изображение'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Сообщество',
    )

    class Meta:
        default_related_name = 'posts'
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-pub_date', 'id']
        indexes = [
            models.Index(
                fields=['pub_date', 'id'],
            )
        ]

    def __str__(self):
        return (f'Публикация: {self.text[:TEXT_DISPLAY_LENGTH]},'
                f'автора: {self.author}.')


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Публикация',
    )
    text = models.TextField('Текст',)
    created = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        default_related_name = 'comments'
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created', 'id']

    def __str__(self):
        return (f'Комментарий: {self.text[:TEXT_DISPLAY_LENGTH]}. '
                f'Автора: {self.author}. '
                f'К публикации: {self.post.text[:TEXT_DISPLAY_LENGTH]}')


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Кто подписан',
        related_name='followers',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='На кого подписан',
        related_name='following',
    )

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_user_following',
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('following')),
                name='prevent_self_follow'
            ),
        ]
        ordering = ['user__username', 'following__username', 'id']
        indexes = [
            models.Index(
                fields=['user', 'following'],
            )
        ]

    def __str__(self):
        return (f'Пользователь: {self.user}, подписан на '
                f'пользователя: {self.following}.')
