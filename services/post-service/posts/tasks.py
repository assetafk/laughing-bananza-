from celery import shared_task
import re
import requests
from django.conf import settings
from .models import Post, Comment, Mention


def extract_mentions(text):
    """Извлекает упоминания пользователей из текста"""
    if not text:
        return []
    pattern = r'@(\w+)'
    matches = re.findall(pattern, text)
    return list(set(matches))


@shared_task
def process_mentions(content_type, content_id):
    """Обрабатывает упоминания в посте или комментарии"""
    try:
        if content_type == 'post':
            content = Post.objects.get(id=content_id)
            text = content.caption
            author_id = content.author_id
        elif content_type == 'comment':
            content = Comment.objects.get(id=content_id)
            text = content.text
            author_id = content.author_id
        else:
            return

        if not text:
            return

        usernames = extract_mentions(text)
        if not usernames:
            return

        # Получаем информацию о пользователях из User Service
        user_service_url = settings.USER_SERVICE_URL
        for username in usernames:
            try:
                # Получаем ID пользователя по username
                response = requests.get(
                    f'{user_service_url}/api/users/',
                    params={'username': username},
                    timeout=5
                )
                if response.status_code == 200:
                    users = response.json().get('results', [])
                    if users:
                        mentioned_user_id = users[0]['id']
                        
                        # Пропускаем, если пользователь упоминает сам себя
                        if mentioned_user_id == author_id:
                            continue

                        # Проверяем, не создано ли уже упоминание
                        mention_exists = False
                        if content_type == 'post':
                            mention_exists = Mention.objects.filter(
                                post=content,
                                mentioned_user_id=mentioned_user_id
                            ).exists()
                        elif content_type == 'comment':
                            mention_exists = Mention.objects.filter(
                                comment=content,
                                mentioned_user_id=mentioned_user_id
                            ).exists()

                        if not mention_exists:
                            # Создаем упоминание
                            mention_data = {
                                'mentioned_user_id': mentioned_user_id,
                                'email_sent': False
                            }
                            if content_type == 'post':
                                mention_data['post'] = content
                            elif content_type == 'comment':
                                mention_data['comment'] = content

                            mention = Mention.objects.create(**mention_data)

                            # Отправляем событие в Notification Service
                            notification_service_url = settings.NOTIFICATION_SERVICE_URL
                            requests.post(
                                f'{notification_service_url}/api/notifications/mentions/',
                                json={'mention_id': mention.id},
                                timeout=5
                            )

            except Exception as e:
                print(f"Error processing mention for {username}: {e}")
                continue

    except (Post.DoesNotExist, Comment.DoesNotExist):
        return
    except Exception as e:
        print(f"Error processing mentions: {e}")
        raise

