from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, Comment
from .tasks import process_mentions
from moderation.tasks import moderate_post, moderate_comment


@receiver(post_save, sender=Post)
def handle_post_save(sender, instance, created, **kwargs):
    """Обработчик сохранения поста"""
    if created:
        # Запускаем обработку упоминаний
        if instance.caption:
            process_mentions.delay('post', instance.id)
        
        # Запускаем модерацию
        moderate_post.delay(instance.id)
    else:
        # Если пост был обновлен и изменилась подпись, обрабатываем упоминания снова
        if instance.caption:
            process_mentions.delay('post', instance.id)


@receiver(post_save, sender=Comment)
def handle_comment_save(sender, instance, created, **kwargs):
    """Обработчик сохранения комментария"""
    if created:
        # Запускаем обработку упоминаний
        if instance.text:
            process_mentions.delay('comment', instance.id)
        
        # Запускаем модерацию
        moderate_comment.delay(instance.id)

