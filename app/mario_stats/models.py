from datetime import datetime

from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=30, unique=True)
    handicap = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.name


class Game(models.Model):
    red_score = models.IntegerField(null=True, blank=True)
    creation_timestamp = models.DateTimeField(default=datetime.now)
    submission_timestamp = models.DateTimeField(null=True, blank=True)
    ian_watched = models.BooleanField(default=False)
    forced_team_selection = models.BooleanField(default=False)

    def __str__(self):
        players = list(self.players.all())
        reds = [player for player in players if player.red_team]
        blues = [player for player in players if not player.red_team]
        red_team = '{} & {}'.format(*reds)
        blue_team = '{} & {}'.format(*blues)

        return f'{red_team} vs {blue_team}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not hasattr(self, 'handicap_snapshot'):
            # First time we save the game, we snapshot everyone's handicaps when it was created
            handicap_snapshot = HandicapSnapshot(game=self)
            handicap_snapshot.save()

            for person in Person.objects.all():
                PlayerHandicapSnapshot(
                    snapshot=handicap_snapshot,
                    person=person,
                    handicap=person.handicap
                ).save()

        return super().save(force_insert, force_update, using, update_fields)


class HandicapSnapshot(models.Model):
    game = models.OneToOneField(Game, on_delete=models.PROTECT, related_name='handicap_snapshot')

    def __str__(self):
        return f'{self.game} ({self.game.creation_timestamp})'


class PlayerHandicapSnapshot(models.Model):
    snapshot = models.ForeignKey(HandicapSnapshot, on_delete=models.PROTECT, related_name='players')
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    handicap = models.DecimalField(max_digits=4, decimal_places=2)


class VehicleClass(models.Model):
    vehicle_type = models.CharField(max_length=10)

    def __str__(self):
        return self.vehicle_type


class VehicleComponent(models.Model):
    name = models.CharField(max_length=30, unique=True)
    speed = models.DecimalField(max_digits=4, decimal_places=2)
    acceleration = models.DecimalField(max_digits=4, decimal_places=2)
    weight = models.DecimalField(max_digits=4, decimal_places=2)
    handling = models.DecimalField(max_digits=4, decimal_places=2)
    grip = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.name


class Vehicle(VehicleComponent):
    vehicle_class = models.ForeignKey(VehicleClass, on_delete=models.PROTECT)


class WeightClass(VehicleComponent):
    pass


class Tyre(VehicleComponent):
    pass


class Glider(VehicleComponent):
    pass


class Character(models.Model):
    name = models.CharField(max_length=20, unique=True)
    weight_class = models.ForeignKey(WeightClass, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Player(models.Model):
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    game = models.ForeignKey(Game, on_delete=models.PROTECT, related_name='players')
    seat_position = models.IntegerField()
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    red_team = models.BooleanField()
    character = models.ForeignKey(Character, on_delete=models.PROTECT)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    tyres = models.ForeignKey(Tyre, on_delete=models.PROTECT)
    glider = models.ForeignKey(Glider, on_delete=models.PROTECT)

    WON = 1
    LOST = 2
    DRAW = 3
    NOT_PLAYED = 4

    outcome_choices = (
        (WON, 'won'),
        (LOST, 'lost'),
        (DRAW, 'draw'),
        (NOT_PLAYED, 'not played'),
    )
    outcome = models.IntegerField(choices=outcome_choices, default=NOT_PLAYED)

    class __meta__:
        unique_together = (
            ('game', 'position'),
            ('game', 'person'),
        )

    def __str__(self):
        return self.person.name
