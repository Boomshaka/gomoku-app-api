from django.test import TestCase, Client


class GameTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_fetch_game_successful(self):
        """Test that game with id exists"""
        new_game = self.client.post('/game/')
        game_id = new_game.data['id']
        game = self.client.get(f'/game/{game_id}')
        self.assertContains(game, game_id, count=1, status_code=200)

    def test_create_game_successful(self):
        """Test creating a new game is successful"""
        game = self.client.post('/game/')
        self.assertContains(game, 'id', status_code=201)
        self.assertEqual(game.data['status'], 'Started')
        self.assertEqual(game.data['winner'], 0)
