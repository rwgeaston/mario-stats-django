from rest_framework.routers import DefaultRouter

from mario_stats.v1.views import GameViewSet

v1_router = DefaultRouter()
v1_router.register(r'games', GameViewSet)
