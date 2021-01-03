from django.test import TestCase, Client


class GameTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_create_game_successful(self):
        """Test creating a new game is successful"""
        game = self.client.post('/game/')
        self.assertContains(game, 'id', status_code=201)
        self.assertEqual(game.data['status'], 'Started')
        self.assertEqual(game.data['winner'], 0)
