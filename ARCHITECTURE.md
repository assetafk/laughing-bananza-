# Архитектура микросервисов

## Обзор

Социальная сеть разбита на следующие микросервисы:

1. **User Service** - управление пользователями и профилями
2. **Post Service** - управление постами и комментариями
3. **Media Service** - обработка изображений (аватары, посты)
4. **Notification Service** - отправка уведомлений
5. **Moderation Service** - модерация контента
6. **API Gateway** - единая точка входа для всех запросов

## Коммуникация между сервисами

- **Синхронная**: HTTP REST API через API Gateway
- **Асинхронная**: RabbitMQ/Kafka для событий (опционально, можно использовать Redis pub/sub)
- **Кеширование**: Redis для кеширования данных

## Технологический стек

- **Backend**: Django + Django REST Framework
- **Message Queue**: Redis (Celery broker)
- **Database**: PostgreSQL (каждый сервис имеет свою БД)
- **Frontend**: React + TypeScript
- **Authentication**: JWT токены

## Схема взаимодействия

```
Frontend (React)
    ↓
API Gateway (Django)
    ↓
┌──────────┬──────────┬──────────┬──────────┬──────────┐
│   User   │   Post   │  Media   │Notification│Moderation│
│ Service  │ Service  │ Service  │  Service  │ Service  │
└──────────┴──────────┴──────────┴──────────┴──────────┘
    ↓         ↓         ↓           ↓           ↓
  PostgreSQL PostgreSQL PostgreSQL PostgreSQL PostgreSQL
```

## Порты сервисов

- API Gateway: 8000
- User Service: 8001
- Post Service: 8002
- Media Service: 8003
- Notification Service: 8004
- Moderation Service: 8005

