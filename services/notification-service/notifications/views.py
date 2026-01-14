from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer
from .tasks import send_mention_email

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return Notification.objects.filter(user_id=user_id)
        return Notification.objects.all()

    @action(detail=False, methods=['post'], url_path='mentions')
    def handle_mention(self, request):
        """Обработка упоминания"""
        mention_id = request.data.get('mention_id')
        if mention_id:
            send_mention_email.delay(mention_id)
            return Response({'status': 'processing'}, status=status.HTTP_202_ACCEPTED)
        return Response({'error': 'mention_id required'}, status=status.HTTP_400_BAD_REQUEST)

