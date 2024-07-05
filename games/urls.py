from django.urls import path
from games import views


urlpatterns = [
    path('', views.hello),
    path('<str:slug_name>', views.indexGame, name='game-detail'),
    path('add-game/', views.add_game, name='add-game'),
]
