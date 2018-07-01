from django.contrib import admin

from .models import (
    Person,
    Game,
    Player,
    Vehicle,
    VehicleClass,
    Tyre,
    Glider,
    WeightClass,
)

admin.site.register(Tyre)
admin.site.register(Glider)
admin.site.register(VehicleClass)
admin.site.register(WeightClass)
admin.site.register(Vehicle)
admin.site.register(Person)


class PlayerInline(admin.StackedInline):
    model = Player
    extra = 4
    max_num = 4


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    inlines = (
        PlayerInline,
    )
