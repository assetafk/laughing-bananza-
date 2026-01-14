from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
from django.conf import settings

@api_view(['POST'])
def auth_token(request):
    """Проксирует запрос на получение токена"""
    user_service_url = settings.USER_SERVICE_URL
    url = f'{user_service_url}/api/auth/token/'
    
    try:
        response = requests.post(url, json=request.data, timeout=10)
        try:
            return Response(response.json(), status=response.status_code)
        except:
            return Response({'error': 'Invalid response from auth service'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except requests.exceptions.RequestException as e:
        return Response({'error': f'Service unavailable: {str(e)}'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def auth_token_refresh(request):
    """Проксирует запрос на обновление токена"""
    user_service_url = settings.USER_SERVICE_URL
    url = f'{user_service_url}/api/auth/token/refresh/'
    
    try:
        response = requests.post(url, json=request.data, timeout=10)
        try:
            return Response(response.json(), status=response.status_code)
        except:
            return Response({'error': 'Invalid response from auth service'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except requests.exceptions.RequestException as e:
        return Response({'error': f'Service unavailable: {str(e)}'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
    # Исправлено: сервисы уже имеют /api/ в пути
    url = f'{base_url}/api/{service}/{path}'
    
    # Передаем заголовки
    headers = {}
    if 'Authorization' in request.headers:
        headers['Authorization'] = request.headers['Authorization']
    
    try:
        # Обработка файлов для POST/PUT/PATCH
        files = None
        data = None
        
        if request.method in ['POST', 'PUT', 'PATCH']:
            if request.content_type and 'multipart/form-data' in request.content_type:
                # Для загрузки файлов
                files = {}
                for key, value in request.FILES.items():
                    files[key] = (value.name, value.read(), value.content_type)
                data = dict(request.data)
                # Удаляем файлы из data, они уже в files
                for key in request.FILES.keys():
                    if key in data:
                        del data[key]
            else:
                data = request.data
        
        # Проксируем запрос
        if request.method == 'GET':
            response = requests.get(url, headers=headers, params=request.query_params, timeout=10)
        elif request.method == 'POST':
            if files:
                response = requests.post(url, headers=headers, files=files, data=data, timeout=10)
            else:
                response = requests.post(url, headers=headers, json=data, timeout=10)
        elif request.method == 'PUT':
            if files:
                response = requests.put(url, headers=headers, files=files, data=data, timeout=10)
            else:
                response = requests.put(url, headers=headers, json=data, timeout=10)
        elif request.method == 'PATCH':
            if files:
                response = requests.patch(url, headers=headers, files=files, data=data, timeout=10)
            else:
                response = requests.patch(url, headers=headers, json=data, timeout=10)
        elif request.method == 'DELETE':
            response = requests.delete(url, headers=headers, timeout=10)
        else:
            return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        # Обработка ответа
        try:
            response_data = response.json()
        except:
            response_data = {'content': response.text}
        
        return Response(response_data, status=response.status_code)
    except requests.exceptions.RequestException as e:
        return Response({'error': f'Service unavailable: {str(e)}'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

