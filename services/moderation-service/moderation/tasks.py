from celery import shared_task
import requests
from django.conf import settings

FORBIDDEN_WORDS = ['spam', 'реклама', 'рекламировать']

def contains_forbidden_words(text):
    if not text:
        return False, []
    text_lower = text.lower()
    found_words = [word for word in FORBIDDEN_WORDS if word.lower() in text_lower]
    return len(found_words) > 0, found_words

def is_spam(text):
    if not text:
        return False
    if len(set(text)) < len(text) * 0.3 and len(text) > 20:
        return True
    if len(text) > 10:
        uppercase_ratio = sum(1 for c in text if c.isupper()) / len(text)
        if uppercase_ratio > 0.5:
            return True
    if 'http://' in text.lower() or 'https://' in text.lower():
        link_count = text.lower().count('http://') + text.lower().count('https://')
        if link_count > 1:
            return True
    return False

@shared_task
def moderate_content(content_type, content_id):
    """Модерирует контент"""
    try:
        post_service_url = settings.POST_SERVICE_URL
        
        # Получаем контент из Post Service
        if content_type == 'post':
            response = requests.get(f'{post_service_url}/api/posts/posts/{content_id}/', timeout=5)
        elif content_type == 'comment':
            response = requests.get(f'{post_service_url}/api/posts/comments/{content_id}/', timeout=5)
        else:
            return
        
        if response.status_code != 200:
            return
        
        content_data = response.json()
        text_to_check = content_data.get('caption') or content_data.get('text', '')
        
        has_forbidden, forbidden_words = contains_forbidden_words(text_to_check)
        is_spam_content = is_spam(text_to_check)
        
        # Определяем статус
        if has_forbidden or is_spam_content:
            status = 'rejected'
            comment_parts = []
            if has_forbidden:
                comment_parts.append(f'Обнаружены запрещенные слова: {", ".join(forbidden_words)}')
            if is_spam_content:
                comment_parts.append('Контент похож на спам')
            moderation_comment = '; '.join(comment_parts)
        else:
            status = 'approved'
            moderation_comment = ''
        
        # Обновляем статус в Post Service
        if content_type == 'post':
            requests.patch(
                f'{post_service_url}/api/posts/posts/{content_id}/',
                json={'moderation_status': status, 'moderation_comment': moderation_comment},
                timeout=5
            )
        elif content_type == 'comment':
            requests.patch(
                f'{post_service_url}/api/posts/comments/{content_id}/',
                json={'moderation_status': status, 'moderation_comment': moderation_comment},
                timeout=5
            )
            
    except Exception as e:
        print(f"Error moderating content: {e}")

