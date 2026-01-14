from celery import shared_task
from PIL import Image
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from io import BytesIO
from .models import Profile


@shared_task
def process_avatar(profile_id):
    """
    Асинхронная обработка аватара:
    - Изменение размера до 400x400
    - Создание миниатюры 150x150
    - Создание маленькой версии 50x50
    - Оптимизация качества
    """
    try:
        profile = Profile.objects.get(id=profile_id)
        
        if not profile.avatar:
            profile.avatar_processing = False
            profile.save(update_fields=['avatar_processing'])
            return

        # Открываем оригинальное изображение
        avatar_path = profile.avatar.path
        img = Image.open(avatar_path)
        
        # Конвертируем в RGB если необходимо (для JPEG)
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        # Размеры для обработки
        sizes = {
            'standard': (400, 400),
            'thumbnail': (150, 150),
            'small': (50, 50)
        }

        # Обрабатываем стандартный размер (400x400)
        img_standard = img.copy()
        img_standard.thumbnail(sizes['standard'], Image.Resampling.LANCZOS)
        
        # Сохраняем стандартный размер (перезаписываем оригинал)
        buffer_standard = BytesIO()
        img_standard.save(buffer_standard, format='JPEG', quality=85, optimize=True)
        buffer_standard.seek(0)
        
        # Обновляем оригинальный файл
        profile.avatar.save(
            os.path.basename(profile.avatar.name),
            ContentFile(buffer_standard.read()),
            save=False
        )

        # Создаем миниатюру 150x150
        img_thumb = img.copy()
        img_thumb.thumbnail(sizes['thumbnail'], Image.Resampling.LANCZOS)
        buffer_thumb = BytesIO()
        img_thumb.save(buffer_thumb, format='JPEG', quality=85, optimize=True)
        buffer_thumb.seek(0)
        
        profile.avatar_thumbnail.save(
            f'thumb_{os.path.basename(profile.avatar.name)}',
            ContentFile(buffer_thumb.read()),
            save=False
        )

        # Создаем маленькую версию 50x50
        img_small = img.copy()
        img_small.thumbnail(sizes['small'], Image.Resampling.LANCZOS)
        buffer_small = BytesIO()
        img_small.save(buffer_small, format='JPEG', quality=80, optimize=True)
        buffer_small.seek(0)
        
        profile.avatar_small.save(
            f'small_{os.path.basename(profile.avatar.name)}',
            ContentFile(buffer_small.read()),
            save=False
        )

        # Сохраняем все изменения и снимаем флаг обработки
        profile.avatar_processing = False
        profile.save()

    except Profile.DoesNotExist:
        return
    except Exception as e:
        # В случае ошибки снимаем флаг обработки
        try:
            profile = Profile.objects.get(id=profile_id)
            profile.avatar_processing = False
            profile.save(update_fields=['avatar_processing'])
        except:
            pass
        raise e

