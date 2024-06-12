from datetime import datetime

from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from gaming.models import Country, Player, Opening, Game


class PlayerTestCase(TestCase):
	def setUp(self):
		country = Country.objects.create(name="Uzbeksitan", prefix="uzb")
		Player.objects.create(name="Mirxojiddin", country=country, wins=10, losses=5, draws=8, elo_rating=1400)

	def test_add_player_db(self):
		player = Player.objects.get(name="Mirxojiddin")
		self.assertEqual(player.name, 'Mirxojiddin')
		self.assertEqual(player.country.name, 'Uzbeksitan')
		self.assertEqual(player.wins, 10)
		self.assertEqual(player.losses, 5)
		self.assertEqual(player.draws, 8)
		self.assertEqual(player.elo_rating, 1400)
		self.assertEqual(player.games_played, 23)

		player.wins = 8
		player.save()
		player = Player.objects.get(name="Mirxojiddin")
		self.assertEqual(player.name, 'Mirxojiddin')
		self.assertEqual(player.country.name, 'Uzbeksitan')
		self.assertEqual(player.wins, 8)
		self.assertEqual(player.losses, 5)
		self.assertEqual(player.draws, 8)
		self.assertEqual(player.elo_rating, 1400)
		self.assertEqual(player.games_played, 21)

	def test_list_player(self):
		url = reverse('gaming:player')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		for data in response.data:
			self.assertEqual(
				list(data.keys()),
				['id', 'name', 'country', 'elo_rating', 'wins', 'losses', 'draws', 'games_played']
			)
		self.assertEqual(response.data[0]['wins'], 10)
		self.assertEqual(response.data[0]['losses'], 5)
		self.assertEqual(response.data[0]['draws'], 8)
		self.assertEqual(response.data[0]['name'], 'Mirxojiddin')
		self.assertEqual(response.data[0]['elo_rating'], 1400)
		self.assertEqual(response.data[0]['games_played'], 23)
		country = Country.objects.get(name="Uzbeksitan")
		Player.objects.create(name="Nurali", country=country, wins=45, losses=52, draws=9, elo_rating=2000)
		response = self.client.get(url)
		for data in response.data:
			self.assertEqual(
							list(data.keys()),
							['id', 'name', 'country', 'elo_rating', 'wins', 'losses', 'draws', 'games_played']
			)
		self.assertEqual(response.data[0]['wins'], 45)
		self.assertEqual(response.data[0]['losses'], 52)
		self.assertEqual(response.data[0]['draws'], 9)
		self.assertEqual(response.data[0]['name'], 'Nurali')
		self.assertEqual(response.data[0]['elo_rating'], 2000)
		self.assertEqual(response.data[0]['games_played'], 106)
		self.assertEqual(response.data[1]['wins'], 10)
		self.assertEqual(response.data[1]['losses'], 5)
		self.assertEqual(response.data[1]['draws'], 8)
		self.assertEqual(response.data[1]['name'], 'Mirxojiddin')
		self.assertEqual(response.data[1]['elo_rating'], 1400)
		self.assertEqual(response.data[1]['games_played'], 23)

	def test_add_player(self):
		url = reverse('gaming:player')
		country = Country.objects.get(name="Uzbeksitan")
		payload = {
			"name": "Nurali",
			"country": country.id,
			"elo_rating": 3000,
			"wins": 10,
			"losses": 12,
			"draws": 16
		}

		response = self.client.post(url, data=payload)
		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.data['wins'], 10)
		self.assertEqual(response.data['losses'], 12)
		self.assertEqual(response.data['draws'], 16)
		self.assertEqual(response.data['name'], 'Nurali')
		self.assertEqual(response.data['elo_rating'], 3000)
		url = reverse('gaming:player')
		response = self.client.get(url)
		for data in response.data:
			self.assertEqual(
							list(data.keys()),
							['id', 'name', 'country', 'elo_rating', 'wins', 'losses', 'draws', 'games_played']
			)
		self.assertEqual(response.data[0]['wins'], 10)
		self.assertEqual(response.data[0]['losses'], 12)
		self.assertEqual(response.data[0]['draws'], 16)
		self.assertEqual(response.data[0]['name'], 'Nurali')
		self.assertEqual(response.data[0]['elo_rating'], 3000)
		self.assertEqual(response.data[0]['games_played'], 38)
		self.assertEqual(response.data[1]['wins'], 10)
		self.assertEqual(response.data[1]['losses'], 5)
		self.assertEqual(response.data[1]['draws'], 8)
		self.assertEqual(response.data[1]['name'], 'Mirxojiddin')
		self.assertEqual(response.data[1]['elo_rating'], 1400)
		self.assertEqual(response.data[1]['games_played'], 23)

	def test_add_player_error(self):
		url = reverse('gaming:player')
		country = Country.objects.get(name="Uzbeksitan")
		payload = {
			"country": country.id,
			"elo_rating": 3000,
			"wins": 10,
			"losses": 12,
			"draws": 16
		}
		response = self.client.post(url, data=payload)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['name'], ['This field is required.'])
		payload = {
			"name": "tojiddin",
			"country": country.id,
			"elo_rating": -3000,
			"wins": -10,
			"losses": 12,
			"draws": 16
		}
		response = self.client.post(url, data=payload)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['elo_rating'], ["Ensure this value is greater than or equal to 0."])
		self.assertEqual(response.json()['wins'], ["Ensure this value is greater than or equal to 0."])

	def test_get_player(self):
		player = Player.objects.get(name="Mirxojiddin")
		url = reverse('gaming:player-detail', kwargs={'pk': player.id})
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['wins'], 10)
		self.assertEqual(response.data['losses'], 5)
		self.assertEqual(response.data['draws'], 8)
		self.assertEqual(response.data['name'], 'Mirxojiddin')
		self.assertEqual(response.data['elo_rating'], 1400)
		self.assertEqual(response.data['games_played'], 23)

	def test_edit_player(self):
		player = Player.objects.get(name="Mirxojiddin")
		payload = {
			"name": "tojiddin",
			"elo_rating": 1200,
			"wins": 20,
			"losses": 12,
			"draws": 16
		}
		url = reverse('gaming:player-detail', kwargs={'pk': player.id})
		response = self.client.put(url, data=payload, content_type='application/json')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['wins'], 20)
		self.assertEqual(response.data['losses'], 12)
		self.assertEqual(response.data['draws'], 16)
		self.assertEqual(response.data['name'], 'tojiddin')
		self.assertEqual(response.data['elo_rating'], 1200)
		payload = {
			"name": "Mirxojiddin",
			"losses": 20,
			"draws": 16
		}
		response = self.client.patch(url, data=payload, content_type='application/json')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['wins'], 20)
		self.assertEqual(response.data['losses'], 20)
		self.assertEqual(response.data['draws'], 16)
		self.assertEqual(response.data['name'], 'Mirxojiddin')
		self.assertEqual(response.data['elo_rating'], 1200)

	def test_filter_player(self):
		url = reverse('gaming:player')
		response = self.client.get(url, params={'name': "Mirxojiddin"})
		self.assertEqual(response.status_code, 200)
		for data in response.data:
			self.assertEqual(
				list(data.keys()),
				['id', 'name', 'country', 'elo_rating', 'wins', 'losses', 'draws', 'games_played']
			)
		self.assertEqual(response.data[0]['wins'], 10)
		self.assertEqual(response.data[0]['losses'], 5)
		self.assertEqual(response.data[0]['draws'], 8)
		self.assertEqual(response.data[0]['name'], 'Mirxojiddin')
		self.assertEqual(response.data[0]['elo_rating'], 1400)
		self.assertEqual(response.data[0]['games_played'], 23)

		response = self.client.get(url, params={'min_elo_rating': "1300"})
		self.assertEqual(response.status_code, 200)
		for data in response.data:
			self.assertEqual(
				list(data.keys()),
				['id', 'name', 'country', 'elo_rating', 'wins', 'losses', 'draws', 'games_played']
			)
		self.assertEqual(response.data[0]['wins'], 10)
		self.assertEqual(response.data[0]['losses'], 5)
		self.assertEqual(response.data[0]['draws'], 8)
		self.assertEqual(response.data[0]['name'], 'Mirxojiddin')
		self.assertEqual(response.data[0]['elo_rating'], 1400)
		self.assertEqual(response.data[0]['games_played'], 23)
		response = self.client.get(url, params={'max_elo_rating': "1500"})
		self.assertEqual(response.status_code, 200)
		for data in response.data:
			self.assertEqual(
				list(data.keys()),
				['id', 'name', 'country', 'elo_rating', 'wins', 'losses', 'draws', 'games_played']
			)
		self.assertEqual(response.data[0]['wins'], 10)
		self.assertEqual(response.data[0]['losses'], 5)
		self.assertEqual(response.data[0]['draws'], 8)
		self.assertEqual(response.data[0]['name'], 'Mirxojiddin')
		self.assertEqual(response.data[0]['elo_rating'], 1400)
		self.assertEqual(response.data[0]['games_played'], 23)
		response = self.client.get(url, params={'max_elo_rating': "1500", 'min_elo_rating': "1300"})
		self.assertEqual(response.status_code, 200)
		for data in response.data:
			self.assertEqual(
				list(data.keys()),
				['id', 'name', 'country', 'elo_rating', 'wins', 'losses', 'draws', 'games_played']
			)
		self.assertEqual(response.data[0]['wins'], 10)
		self.assertEqual(response.data[0]['losses'], 5)
		self.assertEqual(response.data[0]['draws'], 8)
		self.assertEqual(response.data[0]['name'], 'Mirxojiddin')
		self.assertEqual(response.data[0]['elo_rating'], 1400)
		self.assertEqual(response.data[0]['games_played'], 23)
		response = self.client.get(url, params={"country": "Uzbeksitan"})
		self.assertEqual(response.status_code, 200)
		for data in response.data:
			self.assertEqual(
				list(data.keys()),
				['id', 'name', 'country', 'elo_rating', 'wins', 'losses', 'draws', 'games_played']
			)
		self.assertEqual(response.data[0]['wins'], 10)
		self.assertEqual(response.data[0]['losses'], 5)
		self.assertEqual(response.data[0]['draws'], 8)
		self.assertEqual(response.data[0]['name'], 'Mirxojiddin')
		self.assertEqual(response.data[0]['elo_rating'], 1400)
		self.assertEqual(response.data[0]['games_played'], 23)


class CountryTestCase(APITestCase):
	def setUp(self):
		Country.objects.create(name="Uzbeksitan", prefix="uzb")

	def test_list_country(self):
		url = reverse('gaming:country-list')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		for data in response.data:
			self.assertEqual(list(data.keys()), ['id', 'name', 'prefix'])
		self.assertEqual(response.data[0]['id'], 1)
		self.assertEqual(response.data[0]['name'], "Uzbeksitan")
		self.assertEqual(response.data[0]['prefix'], 'uzb')

	def test_order_by_country(self):
		Country.objects.create(name="England", prefix="eng")
		url = reverse('gaming:country-list')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		for data in response.data:
			self.assertEqual(list(data.keys()), ['id', 'name', 'prefix'])
		self.assertEqual(response.data[0]['name'], "England")
		self.assertEqual(response.data[0]['prefix'], 'eng')
		self.assertEqual(response.data[1]['name'], "Uzbeksitan")
		self.assertEqual(response.data[1]['prefix'], 'uzb')


class OpeningTestCase(APITestCase):
	def setUp(self):
		Opening.objects.create(name="Uzbeksitan")

	def test_list_opening(self):
		url = reverse('gaming:opening-list')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data[0]['name'], "Uzbeksitan")


class GameTestCase(APITestCase):
	def setUp(self):
		opening = Opening.objects.create(name="Uzbeksitan")
		country = Country.objects.create(name="Uzbeksitan", prefix="uzb")
		player1 = Player.objects.create(name="Mirxojiddin", country=country, wins=10, losses=5, draws=8, elo_rating=1400)
		player2 = Player.objects.create(name="Tojiddin", country=country, wins=10, losses=5, draws=8, elo_rating=1400)
		Game.objects.create(
			white=player1, black=player2, moves=46,
			date=datetime.now(), result='win', opening=opening
		)

	def test_list_game(self):
		player1 = Player.objects.get(name="Mirxojiddin")
		player2 = Player.objects.get(name="Tojiddin")
		opening = Opening.objects.get(name="Uzbeksitan")
		url = reverse('gaming:game')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		for data in response.data:
			self.assertEqual(
				list(data.keys()),
				['id', 'white', 'black', 'moves', 'date', 'result', 'opening']
			)
		self.assertEqual(response.data[0]['white'], player1.id)
		self.assertEqual(response.data[0]['black'], player2.id)
		self.assertEqual(response.data[0]['moves'], 46)
		self.assertEqual(response.data[0]['result'], 'win')
		self.assertEqual(response.data[0]['opening'], opening.id)
		Game.objects.create(
			white=player2, black=player1, moves=50,
			date=datetime.now(), result='loss', opening=opening
		)
		response = self.client.get(url)
		for data in response.data:
			self.assertEqual(
				list(data.keys()),
				['id', 'white', 'black', 'moves', 'date', 'result', 'opening']
			)
		self.assertEqual(response.data[0]['white'], player1.id)
		self.assertEqual(response.data[0]['black'], player2.id)
		self.assertEqual(response.data[0]['moves'], 46)
		self.assertEqual(response.data[0]['result'], 'win')
		self.assertEqual(response.data[0]['opening'], opening.id)
		self.assertEqual(response.data[1]['white'], player2.id)
		self.assertEqual(response.data[1]['black'], player1.id)
		self.assertEqual(response.data[1]['moves'], 50)
		self.assertEqual(response.data[1]['result'], 'loss')
		self.assertEqual(response.data[1]['opening'], opening.id)

	def test_add_game(self):
		player1 = Player.objects.get(name="Mirxojiddin")
		player2 = Player.objects.get(name="Tojiddin")
		opening = Opening.objects.get(name="Uzbeksitan")
		url = reverse('gaming:game')
		formatted_date = datetime.now().strftime("%Y-%m-%d")
		payload = {
			'white': player1.id,
			'black': player2.id,
			'moves': 47,
			'date': formatted_date,
			'result': "draw",
			'opening': opening.id
		}

		response = self.client.post(url, data=payload)
		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.data['white'], player1.id)
		self.assertEqual(response.data['black'], player2.id)
		self.assertEqual(response.data['moves'], 47)
		self.assertEqual(response.data['result'], 'draw')
		self.assertEqual(response.data['opening'], opening.id)
		response = self.client.get(url)
		for data in response.data:
			self.assertEqual(
				list(data.keys()),
				['id', 'white', 'black', 'moves', 'date', 'result', 'opening']
			)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data[0]['white'], player1.id)
		self.assertEqual(response.data[0]['black'], player2.id)
		self.assertEqual(response.data[0]['moves'], 46)
		self.assertEqual(response.data[0]['result'], 'win')
		self.assertEqual(response.data[0]['opening'], opening.id)
		self.assertEqual(response.data[1]['white'], player1.id)
		self.assertEqual(response.data[1]['black'], player2.id)
		self.assertEqual(response.data[1]['moves'], 47)
		self.assertEqual(response.data[1]['result'], 'draw')
		self.assertEqual(response.data[1]['opening'], opening.id)

	def test_filter_game(self):
		player1 = Player.objects.get(name="Mirxojiddin")
		player2 = Player.objects.get(name="Tojiddin")
		opening = Opening.objects.get(name="Uzbeksitan")
		url = reverse('gaming:game')
		response = self.client.get(url, params={"white_player_name": "Mirxojiddin"})
		self.assertEqual(response.status_code, 200)
		for data in response.data:
			self.assertEqual(
				list(data.keys()),
				['id', 'white', 'black', 'moves', 'date', 'result', 'opening']
			)
		self.assertEqual(response.data[0]['white'], player1.id)
		self.assertEqual(response.data[0]['black'], player2.id)
		self.assertEqual(response.data[0]['moves'], 46)
		self.assertEqual(response.data[0]['result'], 'win')
		self.assertEqual(response.data[0]['opening'], opening.id)
		response = self.client.get(url, params={"black_player_name": "Tojiddin", "white_player_name": "Mirxojiddin"})
		self.assertEqual(response.status_code, 200)
		for data in response.data:
			self.assertEqual(
				list(data.keys()),
				['id', 'white', 'black', 'moves', 'date', 'result', 'opening']
			)
		self.assertEqual(response.data[0]['white'], player1.id)
		self.assertEqual(response.data[0]['black'], player2.id)
		self.assertEqual(response.data[0]['moves'], 46)
		self.assertEqual(response.data[0]['result'], 'win')
		self.assertEqual(response.data[0]['opening'], opening.id)
		response = self.client.get(url, params={"black_player_name": "Tojiddin", })
		self.assertEqual(response.status_code, 200)
		for data in response.data:
			self.assertEqual(
				list(data.keys()),
				['id', 'white', 'black', 'moves', 'date', 'result', 'opening']
			)
		self.assertEqual(response.data[0]['white'], player1.id)
		self.assertEqual(response.data[0]['black'], player2.id)
		self.assertEqual(response.data[0]['moves'], 46)
		self.assertEqual(response.data[0]['result'], 'win')
		self.assertEqual(response.data[0]['opening'], opening.id)
		response = self.client.get(url, params={"result": "win" })
		self.assertEqual(response.status_code, 200)
		for data in response.data:
			self.assertEqual(
				list(data.keys()),
				['id', 'white', 'black', 'moves', 'date', 'result', 'opening']
			)
		self.assertEqual(response.data[0]['white'], player1.id)
		self.assertEqual(response.data[0]['black'], player2.id)
		self.assertEqual(response.data[0]['moves'], 46)
		self.assertEqual(response.data[0]['result'], 'win')
		self.assertEqual(response.data[0]['opening'], opening.id)
		response = self.client.get(url, params={"opening": "Uzbekistan"})
		self.assertEqual(response.status_code, 200)
		for data in response.data:
			self.assertEqual(
				list(data.keys()),
				['id', 'white', 'black', 'moves', 'date', 'result', 'opening']
			)
		self.assertEqual(response.data[0]['white'], player1.id)
		self.assertEqual(response.data[0]['black'], player2.id)
		self.assertEqual(response.data[0]['moves'], 46)
		self.assertEqual(response.data[0]['result'], 'win')
		self.assertEqual(response.data[0]['opening'], opening.id)
