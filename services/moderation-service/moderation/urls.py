from django.urls import path
from .views import moderate

urlpatterns = [
    path('moderate/', moderate, name='moderate'),
]

