from django.contrib import admin
from nested_admin import nested

from .models import (
    Person,
    Game,
    Player,
    Vehicle,
    VehicleClass,
    Tyre,
    Glider,
    WeightClass,
    Character,
    HandicapSnapshot,
    PlayerHandicapSnapshot,
)


class PlayerInline(nested.NestedStackedInline):
    model = Player
    extra = 4
    max_num = 4


class PlayerHandicapSnapshotInline(nested.NestedTabularInline):
    model = PlayerHandicapSnapshot
    extra = 0


class HandicapSnapshotInline(nested.NestedStackedInline):
    model = HandicapSnapshot
    extra = 0
    max_num = 1

    inlines = (
        PlayerHandicapSnapshotInline,
    )


@admin.register(HandicapSnapshot)
class HandicapSnapshotAdmin(nested.NestedModelAdmin):
    inlines = (
        PlayerHandicapSnapshotInline,
    )

    list_display = (
        'game',
        'get_date',
    )

    @staticmethod
    def get_date(obj):
        return obj.game.creation_timestamp
    get_date.short_description = 'Game Date'


@admin.register(Game)
class GameAdmin(nested.NestedModelAdmin):
    inlines = (
        PlayerInline,
        HandicapSnapshotInline,
    )
    list_display = (
        '__str__',
        'red_score',
        'submission_timestamp',
        'ian_watched',
    )
    list_filter = (
        'ian_watched',
    )


vehicle_component_stats = (
    'name',
    'speed',
    'acceleration',
    'weight',
    'handling',
    'grip',
)


class VehicleComponentAdmin(admin.ModelAdmin):
    list_display = vehicle_component_stats

    search_fields = (
        'name',
    )


admin.register(Tyre)(VehicleComponentAdmin)
admin.register(Glider)(VehicleComponentAdmin)
admin.register(WeightClass)(VehicleComponentAdmin)


@admin.register(Vehicle)
class VehicleAdmin(VehicleComponentAdmin):
    list_display = vehicle_component_stats + ('vehicle_class',)

    search_fields = (
        'name',
    )

    list_filter = (
        'vehicle_class',
    )


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'get_weight_class_name',
        'get_speed',
        'get_acceleration',
        'get_weight',
        'get_handling',
        'get_grip',
    )

    search_fields = (
        'name',
    )

    def make_get_attr(attr_name):  # pylint: disable=no-self-argument
        def get_weight_class_attr(self, obj):  # pylint: disable=unused-argument
            return getattr(obj.weight_class, attr_name)
        return get_weight_class_attr

    get_weight_class_name = make_get_attr('name')
    get_weight_class_name.short_description = 'Weight Class'

    get_speed = make_get_attr('speed')
    get_speed.short_description = 'Speed'

    get_acceleration = make_get_attr('acceleration')
    get_acceleration.short_description = 'Acceleration'

    get_weight = make_get_attr('weight')
    get_weight.short_description = 'Weight'

    get_handling = make_get_attr('handling')
    get_handling.short_description = 'Handling'

    get_grip = make_get_attr('grip')
    get_grip.short_description = 'Grip'


admin.site.register(VehicleClass)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'handicap',
        'get_games_played'
    )

    @staticmethod
    def get_games_played(obj):
        return obj.player_set.count()

    get_games_played.short_description = 'Games Played'
