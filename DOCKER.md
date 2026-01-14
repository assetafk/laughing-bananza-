# Docker конфигурация

## Файлы

- `docker-compose.yaml` - полная конфигурация для production со всеми сервисами
- `docker-compose.dev.yaml` - упрощенная версия для разработки

## Запуск

### Production (полная конфигурация)

```bash
docker-compose up -d
```

### Development (упрощенная версия)

```bash
docker-compose -f docker-compose.dev.yaml up -d
```

## Сервисы

### Основные сервисы
- **api-gateway** (8000) - API Gateway
- **user-service** (8001) - User Service
- **post-service** (8002) - Post Service
- **media-service** (8003) - Media Service
- **notification-service** (8004) - Notification Service
- **moderation-service** (8005) - Moderation Service

### Инфраструктура
- **redis** (6379) - Redis для Celery
- **postgres-*** - PostgreSQL базы данных для каждого сервиса

### Workers
- **user-service-worker** - Celery worker для User Service
- **post-service-worker** - Celery worker для Post Service
- **media-service-worker** - Celery worker для Media Service
- **notification-service-worker** - Celery worker для Notification Service
- **moderation-service-worker** - Celery worker для Moderation Service

### Frontend
- **frontend** (3000) - React приложение (закомментирован, раскомментируйте после создания репозитория)

## Примечание

Frontend сервис закомментирован в docker-compose.yaml, так как репозиторий фронтенда должен быть создан отдельно. После создания репозитория `laughing-bananza-frontend` в родительской директории, раскомментируйте секцию `frontend` в docker-compose.yaml.

## Первый запуск

1. Создайте миграции:
```bash
docker-compose exec user-service python manage.py makemigrations
docker-compose exec user-service python manage.py migrate
# Повторите для других сервисов
```

2. Создайте суперпользователя:
```bash
docker-compose exec user-service python manage.py createsuperuser
```

## Остановка

```bash
docker-compose down
```

## Очистка

```bash
docker-compose down -v  # Удаляет volumes
```

