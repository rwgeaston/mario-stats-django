from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from django.urls import path

from .api.v1 import v1_router

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    url(r'api/v1/', include(v1_router.urls)),
    url(r'^_nested_admin/', include('nested_admin.urls')),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    path('api/v1/', include('rwge.urls')),
]
