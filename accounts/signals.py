from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, User
from .tasks import process_avatar


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Создает профиль при создании пользователя"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Profile)
def trigger_avatar_processing(sender, instance, created, **kwargs):
    """Запускает обработку аватара при его изменении"""
    # Проверяем, что аватар был изменен и существует, и обработка еще не запущена
    if instance.avatar and not instance.avatar_processing:
        instance.avatar_processing = True
        instance.save(update_fields=['avatar_processing'])
        # Запускаем асинхронную обработку
        process_avatar.delay(instance.id)

