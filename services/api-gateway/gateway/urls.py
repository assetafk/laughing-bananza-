from django.urls import path, re_path
from .views import proxy_request, auth_token, auth_token_refresh

urlpatterns = [
    # Эндпоинты аутентификации
    path('auth/token/', auth_token, name='auth_token'),
    path('auth/token/refresh/', auth_token_refresh, name='auth_token_refresh'),
    
    # Проксирование к сервисам
    re_path(r'^(?P<service>users|posts|media|notifications|moderation)/(?P<path>.*)$', proxy_request),
    re_path(r'^(?P<service>users|posts|media|notifications|moderation)/$', proxy_request),
]

