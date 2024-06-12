from django.contrib import admin
from gaming.models import Country, Player, Opening, Game


class PlayerAdmin(admin.ModelAdmin):
    list_display = ["name", "country", "games_played"]


class GamiAdmin(admin.ModelAdmin):
    list_display = ["white", "black", "result"]


admin.site.register(Country)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Opening)
admin.site.register(Game, GamiAdmin)
