from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from posts.models import Mention
from .models import Notification


@shared_task
def send_mention_email(mention_id):
    """
    Отправляет email-уведомление пользователю при упоминании.
    
    Args:
        mention_id: ID упоминания
    """
    try:
        mention = Mention.objects.select_related('mentioned_user', 'post', 'comment').get(id=mention_id)
        
        # Проверяем, не было ли уже отправлено уведомление
        if mention.email_sent:
            return

        user = mention.mentioned_user
        
        # Определяем контекст для email
        site_url = getattr(settings, 'SITE_URL', 'http://localhost:8000')
        if mention.post:
            content_type = 'посте'
            content_author = mention.post.author.username
            content_url = f"{site_url}/posts/{mention.post.id}/"
        elif mention.comment:
            content_type = 'комментарии'
            content_author = mention.comment.author.username
            content_url = f"{site_url}/posts/{mention.comment.post.id}/"
        else:
            return

        # Формируем сообщение
        subject = f'Вас упомянули в {content_type}'
        message_text = f'Пользователь @{content_author} упомянул вас в своем {content_type}.\n\n'
        message_text += f'Перейти к {content_type}: {content_url}'

        # Отправляем email
        try:
            send_mail(
                subject=subject,
                message=message_text,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            # Отмечаем, что email отправлен
            mention.email_sent = True
            mention.save(update_fields=['email_sent'])

            # Создаем уведомление в системе
            Notification.objects.create(
                user=user,
                notification_type='mention',
                title=f'Вас упомянули в {content_type}',
                message=f'@{content_author} упомянул вас в своем {content_type}'
            )

        except Exception as e:
            # Логируем ошибку отправки email, но не прерываем выполнение
            print(f"Error sending mention email: {e}")
            # Можно добавить логирование в файл или систему мониторинга

    except Mention.DoesNotExist:
        return
    except Exception as e:
        print(f"Error in send_mention_email task: {e}")
        raise

