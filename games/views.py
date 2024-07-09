from django.shortcuts import render, get_object_or_404, redirect
from .models import Game
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from functools import wraps
from django.views.generic import ListView, DetailView, View, DeleteView, UpdateView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy


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


class GameListView(ListView):
    model = Game
    template_name = 'games/index.html'
    context_object_name = 'games'


game_list = GameListView.as_view()


class GameDetailView(DetailView):
    model = Game
    template_name = 'games/one_game_admin.html'
    context_object_name = 'game'
    slug_url_kwarg = 'slug_name'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.id == 1:
            return super().get(request, *args, **kwargs)
        else:
            return render(request, 'games/one_game.html', {'game': self.object})

    def post(self, request, *args, **kwargs):
        if request.user.id == 1:
            name = request.POST.get("name")
            price = request.POST.get("price")
            description = request.POST.get("description")
            image = request.FILES['upload']
            game = Game(name=name, price=price, description=description, image=image)
            game.save()
            game.create_slug()
            return render(request, 'games/one_game_admin.html', {'game': game})
        else:
            return render(request, 'games/one_game.html', {'game': self.object})


indexGame = login_required(GameDetailView.as_view())


@method_decorator(login_required, name='dispatch')
@method_decorator(user_has_specific_id(id_required=1), name='dispatch')
class AddGameView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'games/add_game.html')

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('upload')
        game = Game(name=name, price=price, description=description, image=image)
        game.save()
        game.create_slug()
        return render(request, 'games/add_game.html')


add_game = AddGameView.as_view()


@method_decorator(login_required, name='dispatch')
@method_decorator(user_has_specific_id(id_required=1), name='dispatch')
class UpdateGameView(UpdateView):
    model = Game
    template_name = 'games/update_game.html'
    fields = ['name', 'price', 'description', 'image']
    slug_url_kwarg = 'slug_name'
    success_url = reverse_lazy('main-page')


update_game = login_required(UpdateGameView.as_view())


@method_decorator(login_required, name='dispatch')
@method_decorator(user_has_specific_id(id_required=1), name='dispatch')
class DeleteGameView(DeleteView):
    model = Game
    template_name = 'games/delete_game.html'
    success_url = reverse_lazy('main-page')
    slug_url_kwarg = 'slug_name'

    def get_object(self, queryset=None):
        return get_object_or_404(Game, slug=self.kwargs.get('slug_name'))


delete_game = login_required(DeleteGameView.as_view())
