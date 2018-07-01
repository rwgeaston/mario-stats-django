from rest_framework import serializers

from mario_stats.models import (
    Game,
    Player,
    Tyre,
    Vehicle,
    Glider,
    Character,
)


class PlayerSerializer(serializers.ModelSerializer):
    person = serializers.StringRelatedField()
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
