from django.shortcuts import render, get_object_or_404, redirect
from .models import Game
from django.http import HttpResponse


def hello(request):
    items = Game.objects.all()
    for game in items:
        game.create_slug()
    context = {
        'games': items
    }
    return render(request, 'games/index.html', context=context)


def indexGame(request, slug_name):
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        image = request.FILES['upload']
        game = Game(name=name, price=price, description=description, image=image)
        game.save()
        game.create_slug()
    game = get_object_or_404(Game, slug=slug_name)
    return render(request, 'games/one_game.html', {'game': game})


def add_game(request):
    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('upload')
        game = Game(name=name, price=price, description=description, image=image)
        game.save()
        game.create_slug()
    return render(request, 'games/add_game.html')


def update_game(request, slug_name):
    game = get_object_or_404(Game, slug=slug_name)
    if request.method == "POST":
        game.name = request.POST.get('name')
        game.price = request.POST.get('price')
        game.description = request.POST.get('description')
        game.image = request.FILES.get('upload', game.image)
        game.save()
        return redirect('main-page')
    context = {
        'game': game
    }
    return render(request, 'games/update_game.html', context=context)


def delete_game(request, slug_name):
    game = get_object_or_404(Game, slug=slug_name)
    if request.method == "POST":
        game.delete()
        return redirect('main-page')
    context = {
        'game': game
    }
    return render(request, 'games/delete_game.html', context=context)
