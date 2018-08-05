from django.db import transaction
from rest_framework import serializers

from mario_stats.models import (
    Game,
    Player,
    Person,
    Tyre,
    Vehicle,
    Glider,
    Character,
)


class PlayerSerializer(serializers.ModelSerializer):
    person = serializers.SlugRelatedField(slug_field='name', queryset=Person.objects.all())
    tyres = serializers.SlugRelatedField(slug_field='name', queryset=Tyre.objects.all())
    vehicle = serializers.SlugRelatedField(slug_field='name', queryset=Vehicle.objects.all())
    glider = serializers.SlugRelatedField(slug_field='name', queryset=Glider.objects.all())
    character = serializers.SlugRelatedField(slug_field='name', queryset=Character.objects.all())

    class Meta:
        model = Player
        exclude = (
            'id',
            'game',
        )


class GameSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True)

    class Meta:
        model = Game
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        players = validated_data.pop('players')
        response = Game.objects.create(**validated_data)
        for player in players:
            player['game'] = response
            Player.objects.create(**player)

        return response


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'
