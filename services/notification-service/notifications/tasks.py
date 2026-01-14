from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import requests
from .models import Notification

@shared_task
def send_mention_email(mention_id):
    """Отправляет email-уведомление при упоминании"""
    try:
        # Получаем информацию о упоминании из Post Service
        post_service_url = settings.POST_SERVICE_URL
        response = requests.get(f'{post_service_url}/api/posts/mentions/{mention_id}/', timeout=5)
        if response.status_code != 200:
            return
        
        mention_data = response.json()
        mentioned_user_id = mention_data.get('mentioned_user_id')
        
        # Получаем информацию о пользователе из User Service
        user_service_url = settings.USER_SERVICE_URL
        user_response = requests.get(f'{user_service_url}/api/users/{mentioned_user_id}/', timeout=5)
        if user_response.status_code != 200:
            return
        
        user_data = user_response.json()
        user_email = user_data.get('email')
        
        # Формируем и отправляем email
        subject = 'Вас упомянули в посте'
        message = f'Пользователь упомянул вас в своем посте.\n\nПерейти: {settings.SITE_URL}/posts/{mention_data.get("post_id")}/'
        
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email], fail_silently=False)
        
        # Создаем уведомление
        Notification.objects.create(
            user_id=mentioned_user_id,
            notification_type='mention',
            title='Вас упомянули',
            message='Вас упомянули в посте'
        )
        
    except Exception as e:
        print(f"Error sending mention email: {e}")

