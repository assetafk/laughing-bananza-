# Интеграция фронтенда с бэкендом

## Что было исправлено

### API Gateway

1. **Эндпоинты аутентификации**
   - Добавлены `/api/auth/token/` и `/api/auth/token/refresh/`
   - Проксируют запросы к User Service

2. **Обработка файлов**
   - Поддержка `multipart/form-data`
   - Корректная передача файлов в Media Service

3. **CORS настройки**
   - Разрешенные методы: GET, POST, PUT, PATCH, DELETE, OPTIONS
   - Разрешенные заголовки: Authorization, Content-Type и др.
   - Поддержка credentials

4. **Обработка ошибок**
   - Обработка недоступных сервисов (503)
   - Корректная обработка JSON ответов

### User Service

1. **Поиск пользователей**
   - Добавлен эндпоинт `/api/users/search/?username=...`
   - Используется для автодополнения при упоминаниях

### Post Service

1. **Улучшена обработка ошибок**
   - Проверка наличия user_id при создании постов/комментариев
   - Выброс `PermissionDenied` при отсутствии авторизации

## Использование API

### Аутентификация

```javascript
// Получение токена
POST /api/auth/token/
Body: { "username": "user", "password": "pass" }
Response: { "access": "...", "refresh": "..." }

// Обновление токена
POST /api/auth/token/refresh/
Body: { "refresh": "..." }
Response: { "access": "..." }
```

### Работа с постами

```javascript
// Получить список постов
GET /api/posts/posts/

// Создать пост
POST /api/posts/posts/
Headers: { "Authorization": "Bearer <token>" }
Body: { "image_url": "...", "caption": "..." }

// Лайкнуть пост
POST /api/posts/posts/{id}/like/
Headers: { "Authorization": "Bearer <token>" }
```

### Загрузка медиа

```javascript
// Загрузить аватар
POST /api/media/upload-avatar/
Headers: { "Authorization": "Bearer <token>" }
Body: FormData с файлом

// Загрузить изображение поста
POST /api/media/upload-post-image/
Headers: { "Authorization": "Bearer <token>" }
Body: FormData с файлом
```

### Поиск пользователей

```javascript
// Поиск по username
GET /api/users/search/?username=john
Response: [{ "id": 1, "username": "john", ... }]
```

## Порты сервисов

- API Gateway: 8000 (основной эндпоинт для фронтенда)
- User Service: 8001
- Post Service: 8002
- Media Service: 8003
- Notification Service: 8004
- Moderation Service: 8005

## Переменные окружения

Для API Gateway:
```env
CORS_ALLOWED_ORIGINS=http://localhost:3000
USER_SERVICE_URL=http://localhost:8001
POST_SERVICE_URL=http://localhost:8002
MEDIA_SERVICE_URL=http://localhost:8003
NOTIFICATION_SERVICE_URL=http://localhost:8004
MODERATION_SERVICE_URL=http://localhost:8005
```

