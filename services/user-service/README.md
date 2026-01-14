# User Service

Микросервис для управления пользователями и профилями.

## API Endpoints

### Аутентификация
- `POST /api/auth/token/` - Получить JWT токен
- `POST /api/auth/token/refresh/` - Обновить JWT токен

### Пользователи
- `POST /api/users/register/` - Регистрация нового пользователя
- `GET /api/users/me/` - Получить текущего пользователя
- `PUT /api/users/update_me/` - Обновить текущего пользователя
- `GET /api/users/{id}/` - Получить пользователя по ID
- `GET /api/users/{id}/profile/` - Получить профиль пользователя

## Запуск

```bash
python manage.py migrate
python manage.py runserver 8001
```

## Переменные окружения

- `DB_NAME` - имя базы данных (по умолчанию: user_service_db)
- `DB_USER` - пользователь БД
- `DB_PASSWORD` - пароль БД
- `DB_HOST` - хост БД
- `DB_PORT` - порт БД
- `CELERY_BROKER_URL` - URL брокера Celery
- `MEDIA_SERVICE_URL` - URL сервиса обработки медиа

