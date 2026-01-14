from celery import shared_task
from posts.models import Post, Comment


# Список запрещенных слов (можно расширить или вынести в настройки/БД)
FORBIDDEN_WORDS = [
    'spam', 'реклама', 'рекламировать',
    # Добавьте другие запрещенные слова по необходимости
]


def contains_forbidden_words(text):
    """
    Проверяет, содержит ли текст запрещенные слова.
    
    Args:
        text: Текст для проверки
        
    Returns:
        tuple: (содержит_запрещенные_слова: bool, найденные_слова: list)
    """
    if not text:
        return False, []
    
    text_lower = text.lower()
    found_words = []
    
    for word in FORBIDDEN_WORDS:
        if word.lower() in text_lower:
            found_words.append(word)
    
    return len(found_words) > 0, found_words


def is_spam(text):
    """
    Простая проверка на спам (можно расширить более сложной логикой).
    
    Args:
        text: Текст для проверки
        
    Returns:
        bool: True если похоже на спам
    """
    if not text:
        return False
    
    # Проверка на повторяющиеся символы (например, "aaaaaa")
    if len(set(text)) < len(text) * 0.3 and len(text) > 20:
        return True
    
    # Проверка на слишком много заглавных букв
    if len(text) > 10:
        uppercase_ratio = sum(1 for c in text if c.isupper()) / len(text)
        if uppercase_ratio > 0.5:
            return True
    
    # Проверка на ссылки (простая)
    if 'http://' in text.lower() or 'https://' in text.lower():
        # Если больше одной ссылки, возможно спам
        link_count = text.lower().count('http://') + text.lower().count('https://')
        if link_count > 1:
            return True
    
    return False


@shared_task
def moderate_post(post_id):
    """
    Модерирует пост в фоновом режиме.
    
    Args:
        post_id: ID поста для модерации
    """
    try:
        post = Post.objects.get(id=post_id)
        
        # Проверяем подпись поста
        text_to_check = post.caption or ''
        
        # Проверка на запрещенные слова
        has_forbidden, forbidden_words = contains_forbidden_words(text_to_check)
        
        # Проверка на спам
        is_spam_content = is_spam(text_to_check)
        
        # Определяем статус модерации
        if has_forbidden or is_spam_content:
            post.moderation_status = 'rejected'
            comment_parts = []
            if has_forbidden:
                comment_parts.append(f'Обнаружены запрещенные слова: {", ".join(forbidden_words)}')
            if is_spam_content:
                comment_parts.append('Контент похож на спам')
            post.moderation_comment = '; '.join(comment_parts)
        else:
            post.moderation_status = 'approved'
            post.moderation_comment = ''
        
        post.save(update_fields=['moderation_status', 'moderation_comment'])
        
    except Post.DoesNotExist:
        return
    except Exception as e:
        print(f"Error moderating post {post_id}: {e}")
        raise


@shared_task
def moderate_comment(comment_id):
    """
    Модерирует комментарий в фоновом режиме.
    
    Args:
        comment_id: ID комментария для модерации
    """
    try:
        comment = Comment.objects.get(id=comment_id)
        
        # Проверяем текст комментария
        text_to_check = comment.text or ''
        
        # Проверка на запрещенные слова
        has_forbidden, forbidden_words = contains_forbidden_words(text_to_check)
        
        # Проверка на спам
        is_spam_content = is_spam(text_to_check)
        
        # Определяем статус модерации
        if has_forbidden or is_spam_content:
            comment.moderation_status = 'rejected'
            comment_parts = []
            if has_forbidden:
                comment_parts.append(f'Обнаружены запрещенные слова: {", ".join(forbidden_words)}')
            if is_spam_content:
                comment_parts.append('Контент похож на спам')
            comment.moderation_comment = '; '.join(comment_parts)
        else:
            comment.moderation_status = 'approved'
            comment.moderation_comment = ''
        
        comment.save(update_fields=['moderation_status', 'moderation_comment'])
        
    except Comment.DoesNotExist:
        return
    except Exception as e:
        print(f"Error moderating comment {comment_id}: {e}")
        raise

