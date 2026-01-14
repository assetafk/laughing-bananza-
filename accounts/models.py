from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


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
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар (оригинал)'
    )
    avatar_thumbnail = models.ImageField(
        upload_to='avatars/thumbnails/',
        blank=True,
        null=True,
        verbose_name='Аватар (миниатюра 150x150)'
    )
    avatar_small = models.ImageField(
        upload_to='avatars/small/',
        blank=True,
        null=True,
        verbose_name='Аватар (маленький 50x50)'
    )
    avatar_processing = models.BooleanField(
        default=False,
        verbose_name='Обработка аватара'
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'Профиль {self.user.username}'

    def get_absolute_url(self):
        return reverse('accounts:profile', kwargs={'username': self.user.username})

