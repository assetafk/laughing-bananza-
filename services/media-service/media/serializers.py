from rest_framework import serializers
from .models import MediaFile


class MediaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = ['id', 'original_url', 'thumbnail_url', 'small_url', 'media_type', 'processing', 'created_at']
        read_only_fields = ['id', 'processing', 'created_at']

