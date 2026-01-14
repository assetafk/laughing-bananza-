from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, Comment
import requests
from django.conf import settings


def trigger_moderation(content_type, content_id):
    """Отправляет запрос на модерацию в Moderation Service"""
    try:
        moderation_service_url = settings.MODERATION_SERVICE_URL
        requests.post(
            f'{moderation_service_url}/api/moderation/moderate/',
            json={'content_type': content_type, 'content_id': content_id},
            timeout=5
        )
    except Exception as e:
        print(f"Error triggering moderation: {e}")


@receiver(post_save, sender=Post)
def handle_post_save(sender, instance, created, **kwargs):
    """Обработчик сохранения поста"""
    if created:
        # Модерация запускается через trigger_moderation в views
        pass


@receiver(post_save, sender=Comment)
def handle_comment_save(sender, instance, created, **kwargs):
    """Обработчик сохранения комментария"""
    if created:
        # Модерация запускается через trigger_moderation в views
        pass

