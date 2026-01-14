# Post Service

Микросервис для управления постами и комментариями.

## API Endpoints

- `GET /api/posts/posts/` - Список постов
- `POST /api/posts/posts/` - Создать пост
- `GET /api/posts/posts/{id}/` - Получить пост
- `POST /api/posts/posts/{id}/add_comment/` - Добавить комментарий
- `POST /api/posts/posts/{id}/like/` - Лайкнуть пост
- `GET /api/posts/comments/` - Список комментариев

## Запуск

```bash
python manage.py migrate
python manage.py runserver 8002
```

## Переменные окружения

- `USER_SERVICE_URL` - URL User Service
- `NOTIFICATION_SERVICE_URL` - URL Notification Service
- `MODERATION_SERVICE_URL` - URL Moderation Service
- `MEDIA_SERVICE_URL` - URL Media Service

