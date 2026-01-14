from django.urls import path, re_path
from .views import proxy_request

urlpatterns = [
    re_path(r'^(?P<service>users|posts|media|notifications|moderation)/(?P<path>.*)$', proxy_request),
    re_path(r'^(?P<service>users|posts|media|notifications|moderation)/$', proxy_request),
]

