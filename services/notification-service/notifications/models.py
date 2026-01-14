from django.db import models

class Notification(models.Model):
    NOTIFICATION_TYPES = [('mention', 'Упоминание'), ('comment', 'Комментарий'), ('like', 'Лайк')]
    user_id = models.IntegerField(verbose_name='ID пользователя')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, verbose_name='Тип уведомления')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    message = models.TextField(verbose_name='Сообщение')
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['-created_at']
        indexes = [models.Index(fields=['user_id', '-created_at']), models.Index(fields=['is_read'])]

