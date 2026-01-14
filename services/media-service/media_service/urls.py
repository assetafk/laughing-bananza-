from django.urls import path, include

urlpatterns = [
    path('api/media/', include('media.urls')),
]

