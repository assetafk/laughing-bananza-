from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя"""
    email = models.EmailField(unique=True, verbose_name='Email')
    bio = models.TextField(max_length=500, blank=True, verbose_name='Биография')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']

    def __str__(self):
        return self.username


class Profile(models.Model):
    """Профиль пользователя с аватаром"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )
    avatar_url = models.URLField(blank=True, null=True, verbose_name='URL аватара')
    avatar_thumbnail_url = models.URLField(blank=True, null=True, verbose_name='URL миниатюры')
    avatar_small_url = models.URLField(blank=True, null=True, verbose_name='URL маленького аватара')
    avatar_processing = models.BooleanField(default=False, verbose_name='Обработка аватара')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'Профиль {self.user.username}'

