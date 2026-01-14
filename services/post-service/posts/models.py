from django.db import models


class Post(models.Model):
    """Модель поста"""
    MODERATION_STATUS_CHOICES = [
        ('pending', 'На модерации'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    ]

    author_id = models.IntegerField(verbose_name='ID автора')
    image_url = models.URLField(verbose_name='URL изображения')
    caption = models.TextField(max_length=2000, blank=True, verbose_name='Подпись')
    moderation_status = models.CharField(
        max_length=20,
        choices=MODERATION_STATUS_CHOICES,
        default='pending',
        verbose_name='Статус модерации'
    )
    moderation_comment = models.TextField(blank=True, null=True, verbose_name='Комментарий модератора')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    likes_count = models.PositiveIntegerField(default=0, verbose_name='Количество лайков')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['moderation_status']),
            models.Index(fields=['author_id']),
        ]

    def __str__(self):
        return f'Пост #{self.id} от пользователя {self.author_id}'


class Comment(models.Model):
    """Модель комментария"""
    MODERATION_STATUS_CHOICES = [
        ('pending', 'На модерации'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    ]

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Пост')
    author_id = models.IntegerField(verbose_name='ID автора')
    text = models.TextField(max_length=1000, verbose_name='Текст комментария')
    moderation_status = models.CharField(
        max_length=20,
        choices=MODERATION_STATUS_CHOICES,
        default='pending',
        verbose_name='Статус модерации'
    )
    moderation_comment = models.TextField(blank=True, null=True, verbose_name='Комментарий модератора')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['post', '-created_at']),
            models.Index(fields=['moderation_status']),
            models.Index(fields=['author_id']),
        ]

    def __str__(self):
        return f'Комментарий #{self.id} от пользователя {self.author_id}'


class Mention(models.Model):
    """Модель упоминания пользователя в посте или комментарии"""
    mentioned_user_id = models.IntegerField(verbose_name='ID упомянутого пользователя')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='mentions',
        null=True,
        blank=True,
        verbose_name='Пост'
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='mentions',
        null=True,
        blank=True,
        verbose_name='Комментарий'
    )
    email_sent = models.BooleanField(default=False, verbose_name='Email отправлен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Упоминание'
        verbose_name_plural = 'Упоминания'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['mentioned_user_id', '-created_at']),
            models.Index(fields=['email_sent']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(post__isnull=False) | models.Q(comment__isnull=False),
                name='mention_must_have_post_or_comment'
            )
        ]

    def __str__(self):
        content_type = 'посту' if self.post else 'комментарию'
        return f'Упоминание пользователя {self.mentioned_user_id} в {content_type}'

