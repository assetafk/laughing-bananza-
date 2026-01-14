from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/<str:username>/', views.ProfileDetailView.as_view(), name='profile'),
    path('profile/edit/', views.profile_update, name='profile_update'),
]

