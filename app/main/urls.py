from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path

from .api.v1 import v1_router

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'api/v1/', include(v1_router.urls)),
]
