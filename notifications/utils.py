import re


def extract_mentions(text):
    """
    Утилита для извлечения упоминаний из текста.
    Ищет паттерн @username
    
    Args:
        text: Текст для анализа
        
    Returns:
        list: Список уникальных имен пользователей
    """
    if not text:
        return []
    
    # Паттерн для поиска упоминаний: @username
    pattern = r'@(\w+)'
    matches = re.findall(pattern, text)
    
    # Убираем дубликаты и возвращаем список уникальных имен пользователей
    return list(set(matches))

