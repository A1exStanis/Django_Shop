from django.contrib import admin

from .models import Game



@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'price_status']
    ordering = ['-price']
    list_editable = ['price']
    search_fields = ['name']
    readonly_fields = ['name', 'slug']

    @admin.display(ordering='price')
    def price_status(self, game: Game):
        if game.price > 1000:
            return 'Expensive'
        if 1000 >= game.price > 300:
            return 'Middle price'
        if game.price <= 300:
            return 'Cheep'
