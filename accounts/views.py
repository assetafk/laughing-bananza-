from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import DetailView
from .models import User, Profile
from .forms import ProfileUpdateForm


@login_required
def profile_update(request):
    """Обновление профиля пользователя"""
    profile = request.user.profile
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('accounts:profile', username=request.user.username)
    else:
        form = ProfileUpdateForm(instance=profile)
    
    return render(request, 'accounts/profile_update.html', {'form': form})


class ProfileDetailView(DetailView):
    """Детальный просмотр профиля"""
    model = User
    template_name = 'accounts/profile_detail.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

