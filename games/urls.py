from django.urls import path

from games import views


urlpatterns = [
    # path('', views.game_list, name='main-page'),
    path('', views.index, name='main-page'),
    path('<str:slug_name>', views.indexGame, name='game-detail'),
    path('add-game/', views.add_game, name='add-game'),
    path('update-game/<str:slug_name>/', views.update_game, name='update-game'),
    path('delete-game/<str:slug_name>/', views.delete_game, name='delete-game'),
    path('success/', views.payment_success, name='success'),
    path('failed/', views.payment_failed, name='failed'),
    path('api/checkout-session/<int:id>', views.create_checkout_session, name='api-checkout-session'),
]
