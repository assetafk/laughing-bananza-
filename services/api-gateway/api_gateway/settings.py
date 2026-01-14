import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-api-gateway-key')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

INSTALLED_APPS = ['django.contrib.contenttypes', 'rest_framework', 'corsheaders', 'gateway']
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware', 'django.middleware.common.CommonMiddleware']
ROOT_URLCONF = 'api_gateway.urls'

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination', 'PAGE_SIZE': 20}

# CORS настройки
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', 'http://localhost:3000').split(',')
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = DEBUG  # Только для разработки

# Разрешенные методы и заголовки
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Service URLs
USER_SERVICE_URL = os.environ.get('USER_SERVICE_URL', 'http://localhost:8001')
POST_SERVICE_URL = os.environ.get('POST_SERVICE_URL', 'http://localhost:8002')
MEDIA_SERVICE_URL = os.environ.get('MEDIA_SERVICE_URL', 'http://localhost:8003')
NOTIFICATION_SERVICE_URL = os.environ.get('NOTIFICATION_SERVICE_URL', 'http://localhost:8004')
MODERATION_SERVICE_URL = os.environ.get('MODERATION_SERVICE_URL', 'http://localhost:8005')

