from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Post, Comment
from .serializers import PostSerializer, PostListSerializer, CommentSerializer
from .tasks import process_mentions
from .signals import trigger_moderation


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet для управления постами"""
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['author_id', 'moderation_status']
    search_fields = ['caption']
    ordering_fields = ['created_at', 'likes_count']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        return PostSerializer

    def get_permissions(self):
        """Разрешения для разных действий"""
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """Фильтруем только одобренные посты для публичного просмотра"""
        queryset = super().get_queryset()
        if self.action in ['list', 'retrieve']:
            # Для публичного просмотра показываем только одобренные
            queryset = queryset.filter(moderation_status='approved')
        return queryset.select_related().prefetch_related('comments')

    def perform_create(self, serializer):
        """Создание поста с автором из токена"""
        # Получаем user_id из JWT токена
        user_id = self.request.user.id if hasattr(self.request, 'user') and self.request.user.is_authenticated else None
        if not user_id:
            # Если нет в токене, пытаемся получить из заголовка
            user_id = self.request.META.get('HTTP_X_USER_ID')
        
        post = serializer.save(author_id=user_id)
        # Запускаем обработку упоминаний
        if post.caption:
            process_mentions.delay('post', post.id)
        # Запускаем модерацию
        trigger_moderation('post', post.id)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_comment(self, request, pk=None):
        """Добавить комментарий к посту"""
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            user_id = request.user.id if hasattr(request, 'user') else request.META.get('HTTP_X_USER_ID')
            comment = serializer.save(post=post, author_id=user_id)
            # Запускаем обработку упоминаний
            if comment.text:
                process_mentions.delay('comment', comment.id)
            # Запускаем модерацию
            trigger_moderation('comment', comment.id)
            return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        """Лайкнуть пост"""
        post = self.get_object()
        post.likes_count += 1
        post.save(update_fields=['likes_count'])
        return Response({'likes_count': post.likes_count})


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для управления комментариями"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]  # Для просмотра

    def get_queryset(self):
        """Фильтруем только одобренные комментарии"""
        return super().get_queryset().filter(moderation_status='approved')

