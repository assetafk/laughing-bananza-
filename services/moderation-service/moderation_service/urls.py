from django.urls import path, include
urlpatterns = [path('api/moderation/', include('moderation.urls'))]

