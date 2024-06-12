from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, RetrieveAPIView, UpdateAPIView
from gaming.models import Country, Player, Game, Opening
from gaming.serializer import PlayerListSerializer, CountryListSerializer, PlayerAddSerializer, \
	PlayerUpdateSerializer, GameListSerializer, GameUpdateSerializer, GameAddSerializer, OpeningListSerializer


class CountryListAPIView(ListAPIView):
	queryset = Country.objects.all()
	serializer_class = CountryListSerializer


class PlayerListAPIView(ListAPIView, CreateAPIView):
	queryset = Player.objects.all()

	def get_serializer_class(self):
		if self.request.method == "GET":
			return PlayerListSerializer
		else:
			return PlayerAddSerializer


class OpeningListAPIView(ListAPIView):
	queryset = Opening.objects.all()
	serializer_class = OpeningListSerializer


class PlayerDetailAPIView(DestroyAPIView, RetrieveAPIView, UpdateAPIView):
	queryset = Player.objects.all()
	lookup_field = "pk"

	def get_serializer_class(self):
		if self.request.method == "PUT" or self.request.method == "PATCH":
			return PlayerUpdateSerializer
		else:
			return PlayerListSerializer


class GameListAPIView(ListAPIView, CreateAPIView):
	queryset = Game.objects.all()

	def get_serializer_class(self):
		if self.request.method == "GET":
			return GameListSerializer
		else:
			return GameAddSerializer


class GameDetailAPIView(DestroyAPIView, RetrieveAPIView, UpdateAPIView):
	queryset = Player.objects.all()
	lookup_field = "pk"

	def get_serializer_class(self):
		if self.request.method == "PUT" or self.request.method == "PATCH":
			return GameUpdateSerializer
		else:
			return GameListSerializer
