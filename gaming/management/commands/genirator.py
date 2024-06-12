import random
from datetime import timedelta, datetime
from django.core.management.base import BaseCommand
from gaming.models import Country, Player, Opening, Game


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        countries = [
            ['Uzbekistan', 'uzb'],
            ['Norway', 'nor'],
            ['France', 'fra'],
            ['Russian', 'rus'],
            ["USA", 'usa'],
            ["Spain", 'spa'],
            ["Italian", 'ita']

        ]
        openings = ['Sicilian Defense', 'French Defense', "Caro-Kann Defense", 'Italian Game',
                    'Scandinavian Defense', 'Spain game']
        results = ['win', 'loss', 'draw']

        for country in countries:
            Country.objects.create(name=country[0], prefix=country[1])

        for opening in openings:
            Opening.objects.create(name=opening)
        country_player = Country.objects.all()
        opening_game = Opening.objects.all()
        players = []
        for i in range(100):  # Create 100 players
            player = Player.objects.create(
                name=f'Player {i+1}',
                elo_rating=random.randint(1200, 2800),
                country=random.choice(country_player),
                wins=0,
                losses=0,
                draws=0
            )
            players.append(player)

        for _ in range(5000):
            white_player = random.choice(players)
            black_player = random.choice(players)
            while black_player == white_player:
                black_player = random.choice(players)

            result = random.choice(results)
            if result == 'win':
                white_player.wins += 1
                black_player.losses += 1
            elif result == 'loss':
                white_player.losses += 1
                black_player.wins += 1
            else:
                white_player.draws += 1
                black_player.draws += 1

            Game.objects.create(
                white=white_player,
                black=black_player,
                result=result,
                opening=random.choice(opening_game),
                moves=random.randint(30, 100),
                date=datetime.now() - timedelta(days=random.randint(0, 1000))
            )

        for player in players:
            player.save()

        self.stdout.write(self.style.SUCCESS('Successfully generated players and games'))
