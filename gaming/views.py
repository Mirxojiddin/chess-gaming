from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, RetrieveAPIView, UpdateAPIView

from gaming.filter import PlayerFilter, GameFilter
from gaming.models import Country, Player, Game, Opening
from gaming.serializer import PlayerListSerializer, CountryListSerializer, PlayerAddSerializer, \
	PlayerUpdateSerializer, GameListSerializer, GameUpdateSerializer, GameAddSerializer, OpeningListSerializer

from django.core.cache import cache
from rest_framework.response import Response

TIME = 600


class CountryListAPIView(ListAPIView):
	queryset = Country.objects.all()
	serializer_class = CountryListSerializer


class PlayerListAPIView(ListAPIView, CreateAPIView):
	queryset = Player.objects.all()
	filter_backends = [DjangoFilterBackend]
	filterset_class = PlayerFilter

	def get_serializer_class(self):
		if self.request.method == "GET":
			return PlayerListSerializer
		else:
			return PlayerAddSerializer

	def get(self, request, *args, **kwargs):
		cache_key = f"players-{request.get_full_path()}"
		cached_data = cache.get(cache_key)
		if not cached_data:
			response = super().get(request, *args, **kwargs)
			cached_data = response.data  # Only cache the data, not the full response
			cache.set(cache_key, cached_data, TIME)
		return Response(cached_data)

	def create(self, request, *args, **kwargs):
		response = super().create(request, *args, **kwargs)
		cache.delete_pattern("players-*")
		return response


class PlayerDetailAPIView(DestroyAPIView, RetrieveAPIView, UpdateAPIView):
	queryset = Player.objects.all()
	lookup_field = "pk"

	def get_serializer_class(self):
		if self.request.method == "PUT" or self.request.method == "PATCH":
			return PlayerUpdateSerializer
		else:
			return PlayerListSerializer

	def get(self, request, *args, **kwargs):
		cache_key = f"player-{kwargs['pk']}"
		cached_data = cache.get(cache_key)
		if not cached_data:
			response = super().get(request, *args, **kwargs)
			cached_data = response.data
			cache.set(cache_key, cached_data, TIME)
		return Response(cached_data)

	def update(self, request, *args, **kwargs):
		print('salom')
		response = super().update(request, *args, **kwargs)
		cache_key = f"player-{kwargs['pk']}"
		cache.delete(cache_key)  # Delete specific cache entry
		cache.delete_pattern("players-*")  # Clear cache related to players list
		return response

	def destroy(self, request, *args, **kwargs):
		response = super().destroy(request, *args, **kwargs)
		cache_key = f"player-{kwargs['pk']}"
		cache.delete(cache_key)  # Delete specific cache entry
		cache.delete_pattern("players-*")  # Clear cache related to players list
		return response


class OpeningListAPIView(ListAPIView):
	queryset = Opening.objects.all()
	serializer_class = OpeningListSerializer


class GameListAPIView(ListAPIView, CreateAPIView):
	queryset = Game.objects.all()
	filter_backends = [DjangoFilterBackend]
	filterset_class = GameFilter

	def get_serializer_class(self):
		if self.request.method == "GET":
			return GameListSerializer
		else:
			return GameAddSerializer

	def get(self, request, *args, **kwargs):
		cache_key = f"games-{request.get_full_path()}"
		cached_data = cache.get(cache_key)
		if not cached_data:
			response = super().get(request, *args, **kwargs)
			cached_data = response.data  # Only cache the data, not the full response
			cache.set(cache_key, cached_data, TIME)
		return Response(cached_data)

	def create(self, request, *args, **kwargs):
		response = super().create(request, *args, **kwargs)
		cache.delete_pattern("games-*")
		return response


class GameDetailAPIView(DestroyAPIView, RetrieveAPIView, UpdateAPIView):
	queryset = Game.objects.all()
	lookup_field = "pk"

	def get_serializer_class(self):
		if self.request.method == "PUT" or self.request.method == "PATCH":
			return GameUpdateSerializer
		else:
			return GameListSerializer

	def get(self, request, *args, **kwargs):
		cache_key = f"game-{kwargs['pk']}"
		cached_data = cache.get(cache_key)
		if not cached_data:
			response = super().get(request, *args, **kwargs)
			cached_data = response.data  # Only cache the data, not the full response
			cache.set(cache_key, cached_data, TIME)
		return Response(cached_data)

	def update(self, request, *args, **kwargs):
		response = super().update(request, *args, **kwargs)
		cache_key = f"game-{kwargs['pk']}"
		cache.delete(cache_key)  # Delete specific cache entry
		cache.delete_pattern("games-*")  # Clear cache related to games list
		return response

	def destroy(self, request, *args, **kwargs):
		response = super().destroy(request, *args, **kwargs)
		cache_key = f"game-{kwargs['pk']}"
		cache.delete(cache_key)  # Delete specific cache entry
		cache.delete_pattern("games-*")  # Clear cache related to games list
		return response
