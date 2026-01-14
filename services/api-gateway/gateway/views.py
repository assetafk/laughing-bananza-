from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
from django.conf import settings

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def proxy_request(request, service, path=''):
    """Проксирует запросы к соответствующим сервисам"""
    service_urls = {
        'users': settings.USER_SERVICE_URL,
        'posts': settings.POST_SERVICE_URL,
        'media': settings.MEDIA_SERVICE_URL,
        'notifications': settings.NOTIFICATION_SERVICE_URL,
        'moderation': settings.MODERATION_SERVICE_URL,
    }
    
    if service not in service_urls:
        return Response({'error': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)
    
    base_url = service_urls[service]
    url = f'{base_url}/api/{service}/{path}'
    
    # Передаем заголовки
    headers = {}
    if 'Authorization' in request.headers:
        headers['Authorization'] = request.headers['Authorization']
    
    try:
        # Проксируем запрос
        if request.method == 'GET':
            response = requests.get(url, headers=headers, params=request.query_params, timeout=10)
        elif request.method == 'POST':
            response = requests.post(url, headers=headers, json=request.data, timeout=10)
        elif request.method == 'PUT':
            response = requests.put(url, headers=headers, json=request.data, timeout=10)
        elif request.method == 'PATCH':
            response = requests.patch(url, headers=headers, json=request.data, timeout=10)
        elif request.method == 'DELETE':
            response = requests.delete(url, headers=headers, timeout=10)
        else:
            return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        return Response(response.json(), status=response.status_code)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

