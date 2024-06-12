from django.urls import path
from gaming.views import CountryListAPIView, PlayerListAPIView, PlayerDetailAPIView, OpeningListAPIView, \
	GameListAPIView, GameDetailAPIView

app_name = 'gaming'

urlpatterns = [
	path('country', CountryListAPIView.as_view(), name='country-list'),
	path('player', PlayerListAPIView.as_view(), name='player'),
	path('player/<int:pk>', PlayerDetailAPIView.as_view(), name='player-detail'),
	path('opening', OpeningListAPIView.as_view(), name='opening-list'),
	path('game', GameListAPIView.as_view(), name='game'),
	path('game/<int:pk>', GameDetailAPIView.as_view(), name='game-detail'),

]
