from celery import shared_task
from PIL import Image
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from io import BytesIO
from .models import MediaFile
from django.conf import settings
import requests


@shared_task
def process_avatar(media_file_id):
    """Обработка аватара"""
    try:
        media_file = MediaFile.objects.get(id=media_file_id)
        
        # Загружаем изображение
        response = requests.get(media_file.original_url)
        img = Image.open(BytesIO(response.content))
        
        # Конвертируем в RGB
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        # Обрабатываем размеры
        sizes = {'thumbnail': (150, 150), 'small': (50, 50)}
        
        for size_name, size in sizes.items():
            img_copy = img.copy()
            img_copy.thumbnail(size, Image.Resampling.LANCZOS)
            buffer = BytesIO()
            img_copy.save(buffer, format='JPEG', quality=85, optimize=True)
            buffer.seek(0)
            
            filename = f'avatars/{size_name}_{os.path.basename(media_file.original_url)}'
            saved_path = default_storage.save(filename, ContentFile(buffer.read()))
            url = f"{settings.MEDIA_URL}{saved_path}"
            
            if size_name == 'thumbnail':
                media_file.thumbnail_url = url
            else:
                media_file.small_url = url

        media_file.processing = False
        media_file.save()

        # Обновляем профиль в User Service
        requests.patch(
            f'{settings.USER_SERVICE_URL}/api/users/{media_file.user_id}/profile/',
            json={
                'avatar_url': media_file.original_url,
                'avatar_thumbnail_url': media_file.thumbnail_url,
                'avatar_small_url': media_file.small_url
            }
        )

    except Exception as e:
        print(f"Error processing avatar: {e}")
        raise


@shared_task
def process_post_image(media_file_id):
    """Обработка изображения поста"""
    try:
        media_file = MediaFile.objects.get(id=media_file_id)
        # Аналогичная обработка для изображений постов
        media_file.processing = False
        media_file.save()
    except Exception as e:
        print(f"Error processing post image: {e}")
        raise

