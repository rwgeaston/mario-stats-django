# pylint: disable=too-many-ancestors
from rest_framework import viewsets
from rest_framework import filters

from mario_stats.models import Game
from mario_stats.models import Person
from .serializers import GameSerializer
from .serializers import PersonSerializer


class GameViewSet(viewsets.ModelViewSet):

    queryset = Game.objects.all()
    serializer_class = GameSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('creation_timestamp',)


class PersonViewSet(viewsets.ModelViewSet):

    queryset = Person.objects.all()
    serializer_class = PersonSerializer
