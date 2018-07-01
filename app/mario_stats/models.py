from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=30)
    handicap = models.DecimalField(max_digits=4, decimal_places=2)


class Game(models.Model):
    red_score = models.IntegerField()
    submission_timestamp = models.DateTimeField()
    ian_watched = models.BooleanField(default=False)
    forced_team_selection = models.BooleanField(default=False)


class HandicapSnapshot(models.Model):
    game = models.ForeignKey(Game, on_delete=models.PROTECT)


class PlayerHandicapSnapshot(models.Model):
    snapshot = models.ForeignKey(HandicapSnapshot, on_delete=models.PROTECT)
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    handicap = models.DecimalField(max_digits=4, decimal_places=2)


class VehicleClass(models.Model):
    vehicle_type = models.CharField(max_length=10)


class StatDifference(models.Model):
    speed = models.DecimalField(max_digits=4, decimal_places=2)
    acceleration = models.DecimalField(max_digits=4, decimal_places=2)
    weight = models.DecimalField(max_digits=4, decimal_places=2)
    handling = models.DecimalField(max_digits=4, decimal_places=2)
    grip = models.DecimalField(max_digits=4, decimal_places=2)


class Vehicle(models.Model):
    name = models.CharField(max_length=20)
    vehicle_class = models.ForeignKey(VehicleClass, on_delete=models.PROTECT)
    stat_difference = models.ForeignKey(StatDifference, on_delete=models.PROTECT)


class WeightClass(models.Model):
    name = models.CharField(max_length=10)
    stat_difference = models.ForeignKey(StatDifference, on_delete=models.PROTECT)


class Tyre(models.Model):
    name = models.CharField(max_length=20)
    stat_difference = models.ForeignKey(StatDifference, on_delete=models.PROTECT)


class Glider(models.Model):
    name = models.CharField(max_length=20)
    stat_difference = models.ForeignKey(StatDifference, on_delete=models.PROTECT)


class Character(models.Model):
    name = models.CharField(max_length=20)
    weight_class = models.ForeignKey(WeightClass, on_delete=models.PROTECT)


class Player(models.Model):
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    position = models.IntegerField()
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    red_team = models.BooleanField()
    character = models.ForeignKey(Character, on_delete=models.PROTECT)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    tyres = models.ForeignKey(Tyre, on_delete=models.PROTECT)
    glider = models.ForeignKey(Glider, on_delete=models.PROTECT)

    class __meta__:
        unique_together = (
            'game',
            'position',
        )
