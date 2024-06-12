
from django.db import models


class Country(models.Model):
	name = models.CharField(max_length=50)
	prefix = models.CharField(max_length=5, null=True)

	def __str__(self):
		return f"{self.name}"

	class Meta:
		ordering = ['name']


class Player(models.Model):
	name = models.CharField(max_length=100)
	elo_rating = models.PositiveIntegerField(default=0)
	country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, related_name='country')
	wins = models.PositiveIntegerField(default=0)
	losses = models.PositiveIntegerField(default=0)
	draws = models.PositiveIntegerField(default=0)
	games_played = models.PositiveIntegerField(default=0, editable=False)

	def __str__(self):
		return f" {self.name}"

	def save(self, *args, **kwargs):
		self.games_played = self.wins + self.losses + self.draws
		super(Player, self).save(*args, **kwargs)

	class Meta:
		ordering = ['-elo_rating']


class Opening(models.Model):
	name = models.CharField(max_length=40)

	def __str__(self):
		return f"{self.name}"


class Game(models.Model):
	RESULTS = [
		('win', 'win'),
		('loss', 'Loss'),
		('draw', 'Draw'),
	]

	white = models.ForeignKey(Player, related_name="white_player", on_delete=models.CASCADE)
	black = models.ForeignKey(Player, related_name="black_player",  on_delete=models.CASCADE)
	moves = models.PositiveIntegerField()
	date = models.DateField()
	result = models.CharField(max_length=4, choices=RESULTS)
	opening = models.ForeignKey(Opening, on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return f"{self.white} vs {self.black}"

