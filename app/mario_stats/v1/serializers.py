from rest_framework import serializers

from mario_stats.models import (
    Game,
    Player,
)


class PlayerSerializer(serializers.ModelSerializer):
    person = serializers.StringRelatedField()
    tyres = serializers.StringRelatedField()
    vehicle = serializers.StringRelatedField()
    glider = serializers.StringRelatedField()
    character = serializers.StringRelatedField()

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
