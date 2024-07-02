from django.shortcuts import render, get_object_or_404
from .models import Game
from django.http import HttpResponse


def hello(request):
    items = Game.objects.all()
    context = {
        'games': items
    }
    return render(request, 'games/index.html', context=context)


def indexGame(request, slug_name):
    game = get_object_or_404(Game, slug=slug_name)
    return render(request, 'games/one_game.html', {'game': game})
