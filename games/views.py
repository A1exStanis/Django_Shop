from django.shortcuts import render, get_object_or_404
from .models import Game, OrderDetail
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from functools import wraps
from django.views.generic import ListView, DetailView, View, DeleteView, UpdateView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseNotFound, JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json, stripe


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


def index(request):
    page_obj = Game.objects.all()

    game_name = request.GET.get('search')
    if game_name != '' and game_name is not None:
        page_obj = page_obj.filter(name__icontains=game_name)

    paginator = Paginator(page_obj, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'games/index.html', context=context)


# class GameListView(ListView):
#     model = Game
#     template_name = 'games/index.html'
#     context_object_name = 'page_obj'
#     paginate_by = 9
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         game_name = self.request.GET.get('search')
#         if game_name:
#             queryset = queryset.filter(name__icontains=game_name)
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['search'] = self.request.GET.get('search', '')
#         return context
#
#
# game_list = GameListView.as_view()


class GameDetailView(DetailView):
    model = Game
    template_name = 'games/one_game_admin.html'
    context_object_name = 'game'
    slug_url_kwarg = 'slug_name'
    pk_url_kwarg = 'pk'

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

    def get_context_data(self, **kwargs):
        context = super(GameDetailView, self).get_context_data(**kwargs)
        context['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context


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


@csrf_exempt
@method_decorator(login_required, name='dispatch')
def create_checkout_session(request, id):
    product = get_object_or_404(Game, pk=id)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        customer_email=request.user.email,
        payment_method_types=['card'],
        line_games=[
            {'price_data': {
                'currency': 'uah',
                'product_data': {
                    'name': product.name,
                },
                'unit_amount': int(product.price)
            },
                'quantity': 1,
            }
        ],
        mode='payment',
        success_url=request.built_absolute_uri(reverse('success'))+'?session_id+{CHECKOUT_SESSION_ID}',
        cancel_url=request.built_absolute_uri(reverse('failed'))
    )
    order = OrderDetail()
    order.customer_name = request.user.name
    order.product = product
    order.stripe_payment_intent = checkout_session['payment_intent']
    order.amount = int(product.price)
    order.save()
    return JsonResponse({'sessionId': checkout_session.id})
