from rest_framework import serializers
from .models import Post, Comment, Mention


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментария"""
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author_id', 'text', 'moderation_status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'moderation_status', 'created_at', 'updated_at']


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор поста"""
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'author_id', 'image_url', 'caption', 'moderation_status',
            'moderation_comment', 'created_at', 'updated_at', 'likes_count',
            'comments', 'comments_count'
        ]
        read_only_fields = ['id', 'moderation_status', 'moderation_comment', 'created_at', 'updated_at', 'likes_count']

    def create(self, validated_data):
        # Получаем author_id из токена
        request = self.context.get('request')
        if request and hasattr(request, 'user_id'):
            validated_data['author_id'] = request.user_id
        return super().create(validated_data)


class PostListSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор для списка постов"""
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'author_id', 'image_url', 'caption', 'moderation_status',
            'created_at', 'likes_count', 'comments_count'
        ]


class MentionSerializer(serializers.ModelSerializer):
    """Сериализатор упоминания"""
    class Meta:
        model = Mention
        fields = ['id', 'mentioned_user_id', 'post', 'comment', 'email_sent', 'created_at']
        read_only_fields = ['id', 'email_sent', 'created_at']

