from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .tasks import moderate_content

@api_view(['POST'])
def moderate(request):
    """Эндпоинт для запуска модерации"""
    content_type = request.data.get('content_type')
    content_id = request.data.get('content_id')
    
    if not content_type or not content_id:
        return Response({'error': 'content_type and content_id required'}, status=status.HTTP_400_BAD_REQUEST)
    
    moderate_content.delay(content_type, content_id)
    return Response({'status': 'processing'}, status=status.HTTP_202_ACCEPTED)

