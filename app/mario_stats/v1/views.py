# pylint: disable=too-many-ancestors
from rest_framework import viewsets

from mario_stats.models import Game
from .serializers import GameSerializer


class GameViewSet(viewsets.ModelViewSet):

    queryset = Game.objects.all()
    serializer_class = GameSerializer
