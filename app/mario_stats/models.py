from datetime import datetime
from decimal import Decimal

from django.db import models
from django.conf import settings

from .game_outcomes import calculate_scores_needed


def current_average_handicap():
    sum_handicaps = 0
    count_people = 0
    for person in Person.objects.all():
        sum_handicaps += person.handicap
        count_people += 1
    if not count_people:
        return Decimal('0.0')

    return Decimal(sum_handicaps/count_people)


class Person(models.Model):
    name = models.CharField(max_length=30, unique=True)
    handicap = models.DecimalField(max_digits=4, decimal_places=2, default=current_average_handicap)

    def __str__(self):
        return self.name


class Game(models.Model):
    red_score = models.IntegerField(null=True, blank=True)
    creation_timestamp = models.DateTimeField(default=datetime.now)
    submission_timestamp = models.DateTimeField(null=True, blank=True)
    ian_watched = models.BooleanField(default=False)
    forced_team_selection = models.BooleanField(default=False)

    RED_WON = 1
    BLUE_WON = 2
    DRAW = 3
    NOT_PLAYED = 4

    outcome_choices = (
        (RED_WON, 'won'),
        (BLUE_WON, 'lost'),
        (DRAW, 'draw'),
        (NOT_PLAYED, 'not played'),
    )
    outcome = models.IntegerField(choices=outcome_choices, default=NOT_PLAYED)

    def __str__(self):
        players = list(self.players.all())
        reds = [player for player in players if player.red_team]
        blues = [player for player in players if not player.red_team]
        red_team = ' & '.join([str(player) for player in reds])
        blue_team = ' & '.join([str(player) for player in blues])

        return f'{red_team} vs {blue_team}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.red_score and self.outcome == self.NOT_PLAYED:
            if not self.submission_timestamp:
                self.submission_timestamp = datetime.now()

            needed_scores = self.get_scores_needed()
            blue_score = 410 - self.red_score
            players = list(self.players.all())
            if self.red_score >= needed_scores['to win']['red']:
                self.outcome = self.RED_WON
                if self.red_score >= needed_scores['to change']['red']:
                    self.change_handicaps(players)
            elif blue_score >= needed_scores['to win']['blue']:
                self.outcome = self.BLUE_WON
                if blue_score >= needed_scores['to change']['blue']:
                    self.change_handicaps(players)
            else:
                self.outcome = self.DRAW

            self.set_player_outcomes(players)

            for player in players:
                player.save()

            self.check_handicap_decay()

        response = super().save(force_insert, force_update, using, update_fields)
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

        return response

    def get_scores_needed(self):
        return calculate_scores_needed(self)

    def change_handicaps(self, players):
        # Do not call this unless winning score was enough to change handicaps!
        # It doesn't recheck that's true
        computer_handicap = 0
        for player in players:
            if player.red_team is (self.outcome == self.RED_WON):
                player.person.handicap += Decimal('0.25')
            else:
                player.person.handicap -= Decimal('0.25')
            player.person.save()

            if player.person.name == 'Computer':
                computer_handicap = player.person.handicap

        # If computer handicap is non-zero we have to go change everyone now :(
        if computer_handicap:
            for person in Person.objects.all():
                person.handicap -= computer_handicap
                person.save()

    def set_player_outcomes(self, players):
        for player in players:
            if self.outcome in [self.DRAW, self.NOT_PLAYED]:
                player.outcome = self.outcome
            elif player.red_team is (self.outcome == self.RED_WON):
                player.outcome = player.WON
            else:
                player.outcome = player.LOST

    def check_handicap_decay(self):
        games_generated = self.__class__.objects.count()
        if games_generated >= settings.START_DECAYING_AT and games_generated % 10 == 0:
            self.decay_not_recent_players(50)

    def decay_not_recent_players(self, game_count):
        players_last_fifty_games = self.get_recent_players(game_count)
        for person in Person.objects.all():
            if person.id in players_last_fifty_games:
                continue

            if person.handicap <= 0:
                continue

            person.handicap -= Decimal('0.25')
            person.save()

    def get_recent_players(self, game_count):
        all_recent_players = set()
        for _, game in zip(
                range(game_count),
                self.__class__.objects.all().order_by('-creation_timestamp')
        ):
            for player in game.players.all():
                all_recent_players.add(player.person.id)
        return all_recent_players


class HandicapSnapshot(models.Model):
    game = models.OneToOneField(Game, on_delete=models.CASCADE, related_name='handicap_snapshot')

    def __str__(self):
        return f'{self.game} ({self.game.creation_timestamp})'


class PlayerHandicapSnapshot(models.Model):
    snapshot = models.ForeignKey(HandicapSnapshot, on_delete=models.CASCADE, related_name='players')
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
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='players')
    seat_position = models.IntegerField()
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
