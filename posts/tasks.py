from celery import shared_task
import re
from django.contrib.auth import get_user_model
from .models import Post, Comment, Mention
from notifications.tasks import send_mention_email

User = get_user_model()


def extract_mentions(text):
    """
    Извлекает упоминания пользователей из текста.
    Ищет паттерн @username
    """
    if not text:
        return []
    
    # Паттерн для поиска упоминаний: @username (username может содержать буквы, цифры, подчеркивания)
    pattern = r'@(\w+)'
    matches = re.findall(pattern, text)
    
    # Убираем дубликаты и возвращаем список уникальных имен пользователей
    return list(set(matches))


@shared_task
def process_mentions(content_type, content_id):
    """
    Обрабатывает упоминания в посте или комментарии.
    
    Args:
        content_type: 'post' или 'comment'
        content_id: ID поста или комментария
    """
    try:
        if content_type == 'post':
            content = Post.objects.get(id=content_id)
            text = content.caption
        elif content_type == 'comment':
            content = Comment.objects.get(id=content_id)
            text = content.text
        else:
            return

        if not text:
            return

        # Извлекаем упоминания из текста
        usernames = extract_mentions(text)

        if not usernames:
            return

        # Создаем записи Mention для каждого упомянутого пользователя
        for username in usernames:
            try:
                mentioned_user = User.objects.get(username=username)
                
                # Пропускаем, если пользователь упоминает сам себя
                if content_type == 'post' and content.author == mentioned_user:
                    continue
                elif content_type == 'comment' and content.author == mentioned_user:
                    continue

                # Проверяем, не создано ли уже упоминание
                mention_exists = False
                if content_type == 'post':
                    mention_exists = Mention.objects.filter(
                        post=content,
                        mentioned_user=mentioned_user
                    ).exists()
                elif content_type == 'comment':
                    mention_exists = Mention.objects.filter(
                        comment=content,
                        mentioned_user=mentioned_user
                    ).exists()

                if not mention_exists:
                    # Создаем упоминание
                    mention_data = {
                        'mentioned_user': mentioned_user,
                        'email_sent': False
                    }
                    if content_type == 'post':
                        mention_data['post'] = content
                    elif content_type == 'comment':
                        mention_data['comment'] = content

                    mention = Mention.objects.create(**mention_data)

                    # Отправляем email-уведомление
                    send_mention_email.delay(mention.id)

            except User.DoesNotExist:
                # Пользователь с таким username не найден, пропускаем
                continue

    except (Post.DoesNotExist, Comment.DoesNotExist):
        return
    except Exception as e:
        # Логируем ошибку, но не прерываем выполнение
        print(f"Error processing mentions: {e}")
        raise

