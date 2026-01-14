from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from posts.models import Post


def home(request):
    """Главная страница"""
    if request.user.is_authenticated:
        # Для авторизованных пользователей показываем последние посты
        posts = Post.objects.filter(moderation_status='approved').select_related('author')[:10]
        return render(request, 'social_network/home.html', {'posts': posts})
    else:
        # Для неавторизованных - приветственная страница
        return render(request, 'social_network/welcome.html')
    print('Home page loaded')

