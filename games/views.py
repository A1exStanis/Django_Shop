from django.shortcuts import render, get_object_or_404, redirect
from .models import Game
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from functools import wraps


def user_has_specific_id(id_required):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.id == id_required:
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied
        return wrapper
    return decorator


def hello(request):
    items = Game.objects.all()
    for game in items:
        game.create_slug()
    context = {
        'games': items
    }
    return render(request, 'games/index.html', context=context)


def indexGame(request, slug_name):
    user_id = request.user.id
    if user_id == 1:
        if request.method == "POST":
            name = request.POST.get("name")
            price = request.POST.get("price")
            description = request.POST.get("description")
            image = request.FILES['upload']
            game = Game(name=name, price=price, description=description, image=image)
            game.save()
            game.create_slug()
        game = get_object_or_404(Game, slug=slug_name)
        return render(request, 'games/one_game_admin.html', {'game': game})
    else:
        game = get_object_or_404(Game, slug=slug_name)
        return render(request, 'games/one_game.html', {'game': game})


@login_required
@user_has_specific_id(id_required=1)
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


@login_required
@user_has_specific_id(id_required=1)
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


@login_required
@user_has_specific_id(id_required=1)
def delete_game(request, slug_name):
    game = get_object_or_404(Game, slug=slug_name)
    if request.method == "POST":
        game.delete()
        return redirect('main-page')
    context = {
        'game': game
    }
    return render(request, 'games/delete_game.html', context=context)
