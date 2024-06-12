from rest_framework import serializers
from gaming.models import Country, Player, Opening, Game


class CountryListSerializer(serializers.ModelSerializer):

	class Meta:
		model = Country
		fields = ['id', 'name', 'prefix']


class PlayerListSerializer(serializers.ModelSerializer):
	country = serializers.CharField(source='country.name')

	class Meta:
		model = Player
		fields = ['id', 'name', 'country', 'elo_rating', 'wins', 'losses', 'draws', 'games_played']


class PlayerAddSerializer(serializers.ModelSerializer):

	class Meta:
		model = Player
		fields = ['name', 'country', 'elo_rating', 'wins', 'losses', 'draws']


class PlayerUpdateSerializer(serializers.ModelSerializer):

	class Meta:
		model = Player
		fields = ['name', 'elo_rating', 'wins', 'losses', 'draws']


class OpeningListSerializer(serializers.ModelSerializer):

	class Meta:
		model = Opening
		fields = ['id', 'name']


class GameListSerializer(serializers.ModelSerializer):
	white = serializers.CharField(source='white.name')
	black = serializers.CharField(source='black.name')
	opening = serializers.CharField(source='opening.name')

	class Meta:
		model = Game
		fields = ['id', 'white', 'black', 'moves', 'date', 'result', 'opening']


class GameAddSerializer(serializers.ModelSerializer):

	class Meta:
		model = Game
		fields = ['white', 'black', 'moves', 'date', 'result', 'opening']


class GameUpdateSerializer(serializers.ModelSerializer):

	class Meta:
		model = Game
		fields = ['moves', 'date', 'result', 'opening']