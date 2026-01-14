# Социальная сеть на Django и Celery

Социальная сеть с функциями:
- Отправка email-уведомлений при упоминании пользователя (@user)
- Асинхронная загрузка и обработка аватаров, создание миниатюр
- Модерация комментариев и постов в фоновом режиме

## Технологический стек

- **Django** 4.2+ - веб-фреймворк
- **Celery** 5.3+ - асинхронная обработка задач
- **Redis** - брокер сообщений для Celery
- **Pillow** - обработка изображений
- **SQLite** - база данных для разработки (PostgreSQL для production)

## Установка

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd laughing-bananza-
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

Скопируйте `.env.example` в `.env` и заполните необходимые значения:

```bash
cp .env.example .env
```

### 5. Применение миграций

```bash
python manage.py migrate
```

### 6. Создание суперпользователя

```bash
python manage.py createsuperuser
```

### 7. Запуск Redis

Убедитесь, что Redis запущен:

```bash
# На macOS с Homebrew
brew services start redis

# На Linux
sudo systemctl start redis

# Или через Docker
docker run -d -p 6379:6379 redis
```

### 8. Запуск Celery Worker

В отдельном терминале:

```bash
celery -A social_network worker --loglevel=info
```

### 9. Запуск Django сервера

```bash
python manage.py runserver
```

## Структура проекта

```
social_network/
├── accounts/          # Управление пользователями и профилями
│   ├── models.py      # User, Profile
│   ├── tasks.py       # Обработка аватаров
│   └── signals.py     # Сигналы для обработки аватаров
├── posts/             # Посты и комментарии
│   ├── models.py      # Post, Comment, Mention
│   ├── tasks.py       # Обработка упоминаний
│   └── signals.py     # Сигналы для упоминаний и модерации
├── notifications/     # Уведомления
│   ├── models.py      # Notification
│   └── tasks.py       # Отправка email-уведомлений
└── moderation/        # Модерация контента
    └── tasks.py       # Фоновая модерация постов и комментариев
```

## Основные функции

### 1. Email-уведомления при упоминаниях

При упоминании пользователя в посте или комментарии через `@username`:
- Автоматически создается запись `Mention`
- Отправляется email-уведомление пользователю
- Создается уведомление в системе

### 2. Асинхронная обработка аватаров

При загрузке аватара:
- Создается стандартная версия 400x400
- Создается миниатюра 150x150
- Создается маленькая версия 50x50
- Все версии оптимизируются для веб

### 3. Фоновая модерация контента

При создании поста или комментария:
- Проверка на запрещенные слова
- Проверка на спам
- Автоматическое одобрение или отклонение

## Использование

### Создание поста

1. Войдите в систему
2. Перейдите на `/posts/create/`
3. Загрузите изображение и добавьте подпись
4. Пост автоматически отправляется на модерацию

### Упоминание пользователя

В подписи поста или комментарии используйте `@username`:

```
Отличный пост! @john, посмотри на это!
```

### Просмотр уведомлений

Перейдите на `/notifications/` для просмотра всех уведомлений.

## Настройка email

Для отправки реальных email-уведомлений настройте SMTP в `.env`:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@socialnetwork.com
```

## Production


1. Использовать PostgreSQL вместо SQLite
2. Настроить правильные `ALLOWED_HOSTS`
3. Использовать безопасный `SECRET_KEY`
4. Настроить статические файлы через Nginx или CDN
5. Настроить мониторинг Celery задач
6. Использовать supervisor или systemd для управления процессами

## Лицензия

MIT

