from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import MediaFile
from .serializers import MediaFileSerializer
from .tasks import process_avatar, process_post_image


class MediaViewSet(viewsets.ModelViewSet):
    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer
    parser_classes = [MultiPartParser, FormParser]

    @action(detail=False, methods=['post'], url_path='upload-avatar')
    def upload_avatar(self, request):
        """Загрузка аватара"""
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'Файл не предоставлен'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Сохраняем файл
        import os
        from django.core.files.storage import default_storage
        filename = default_storage.save(f'avatars/{file.name}', file)
        file_url = request.build_absolute_uri(default_storage.url(filename))
        
        # Создаем запись
        media_file = MediaFile.objects.create(
            original_url=file_url,
            media_type='avatar',
            processing=True
        )
        
        # Запускаем обработку
        process_avatar.delay(media_file.id)
        
        return Response(MediaFileSerializer(media_file).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='upload-post-image')
    def upload_post_image(self, request):
        """Загрузка изображения для поста"""
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'Файл не предоставлен'}, status=status.HTTP_400_BAD_REQUEST)
        
        import os
        from django.core.files.storage import default_storage
        filename = default_storage.save(f'posts/{file.name}', file)
        file_url = request.build_absolute_uri(default_storage.url(filename))
        
        media_file = MediaFile.objects.create(
            original_url=file_url,
            media_type='post_image',
            processing=True
        )
        
        process_post_image.delay(media_file.id)
        
        return Response(MediaFileSerializer(media_file).data, status=status.HTTP_201_CREATED)

