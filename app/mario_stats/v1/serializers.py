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
    HandicapSnapshot,
    PlayerHandicapSnapshot,
)


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        fields = self.context['request'].query_params.get('fields')
        if fields:
            fields = fields.split(',')
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


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


class PlayerHandicapSnapshotSerializer(serializers.ModelSerializer):
    person = serializers.SlugRelatedField(slug_field='name', queryset=Person.objects.all())

    class Meta:
        model = PlayerHandicapSnapshot
        exclude = (
            'snapshot',
        )


class HandicapSnapshotSerializer(serializers.ModelSerializer):
    players = PlayerHandicapSnapshotSerializer(many=True)

    class Meta:
        model = HandicapSnapshot
        exclude = (
            'game',
        )


class GameSerializer(DynamicFieldsModelSerializer):
    players = PlayerSerializer(many=True)
    handicap_snapshot = HandicapSnapshotSerializer(read_only=True)
    scores_needed = serializers.SerializerMethodField()

    @staticmethod
    def get_scores_needed(game):
        return game.get_scores_needed()

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
