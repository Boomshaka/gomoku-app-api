from django.test import TestCase, Client
from game.models import Game
# from game.serializers import GameSerializer
# from unittest.mock import patch


class GameTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_create_game_successful(self):
        """Test creating a new game is successful"""
        game = self.client.post('/game/')
        self.assertContains(game, 'id', status_code=201)
        self.assertEqual(2, game.data['grid'][7][7])
        self.assertEqual(game.data['status'], 'Started')
        self.assertEqual(game.data['winner'], 0)

    def test_fetch_game_successful(self):
        """Test that game with id exists"""
        new_game = self.client.post('/game/')
        game_id = new_game.data['id']
        game = self.client.get(f'/game/{game_id}/')
        self.assertContains(game, game_id, count=1, status_code=200)

    def test_make_move_successful(self):
        """Test that game piece can be placed in grid with PUT request"""
        game = self.client.post('/game/')
        game_id = game.data['id']
        payload = {'row': 8, 'col': 7, 'skip_AI': True}
        res = self.client.put(
            f'/game/{game_id}/',
            data=payload,
            content_type='application/json'
        )
        self.assertIn(1, res.data['grid'][8])
        self.assertEqual(res.data['status'], 'Playing')
        self.assertEqual(res.data['winner'], 0)

    def test_invalid_index_col(self):
        """Test that invalid col index returns an index error"""
        game = self.client.post('/game/')
        game_id = game.data['id']
        payload = {'row': 0, 'col': -1, 'skip_AI': True}
        res = self.client.put(
            f'/game/{game_id}/',
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 400)

    def test_invalid_index_row(self):
        """Test that invalid row index returns an index error"""
        game = self.client.post('/game/')
        game_id = game.data['id']
        payload = {'row': -1, 'col': 0, 'skip_AI': True}
        res = self.client.put(
            f'/game/{game_id}/',
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 400)

    def test_index_exists(self):
        """Test that making a move in index with preexisting piece fails"""
        game = self.client.post('/game/')
        game_id = game.data['id']
        payload = {'row': 0, 'col': 0, 'skip_AI': True}
        self.client.put(
            f'/game/{game_id}/',
            data=payload,
            content_type='application/json'
        )
        res = self.client.put(
            f'/game/{game_id}/',
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 400)

    def test_winner_col(self):
        """Test for winner when there's vertical 5"""
        game = self.client.post('/game/')
        game_id = game.data['id']
        payload = [
            {'row': 0, 'col': 0, 'skip_AI': True},
            {'row': 0, 'col': 1, 'skip_AI': True},
            {'row': 0, 'col': 2, 'skip_AI': True},
            {'row': 0, 'col': 3, 'skip_AI': True},
            {'row': 0, 'col': 4, 'skip_AI': True}
        ]
        res = None
        for p in payload:
            res = self.client.put(
                f'/game/{game_id}/',
                data=p,
                content_type='application/json'
            )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['status'], 'Finished')
        self.assertEqual(res.data['winner'], 1)

    def test_winner_row(self):
        """Test for winner when there's horizontal 5"""
        game = self.client.post('/game/')
        game_id = game.data['id']
        payload = [
            {'row': 0, 'col': 0, 'skip_AI': True},
            {'row': 1, 'col': 0, 'skip_AI': True},
            {'row': 2, 'col': 0, 'skip_AI': True},
            {'row': 3, 'col': 0, 'skip_AI': True},
            {'row': 4, 'col': 0, 'skip_AI': True}
        ]
        res = None
        for p in payload:
            res = self.client.put(
                f'/game/{game_id}/',
                data=p,
                content_type='application/json'
            )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['status'], 'Finished')
        self.assertEqual(res.data['winner'], 1)

    def test_winner_diagonal(self):
        """Test for winner when there's diagonal 5"""
        game = self.client.post('/game/')
        game_id = game.data['id']
        payload = [
            {'row': 0, 'col': 0, 'skip_AI': True},
            {'row': 1, 'col': 1, 'skip_AI': True},
            {'row': 2, 'col': 2, 'skip_AI': True},
            {'row': 3, 'col': 3, 'skip_AI': True},
            {'row': 4, 'col': 4, 'skip_AI': True}
        ]
        res = None
        for p in payload:
            res = self.client.put(
                f'/game/{game_id}/',
                data=p,
                content_type='application/json'
            )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['status'], 'Finished')
        self.assertEqual(res.data['winner'], 1)

    def test_AI_make_move_successful(self):
        """Test that AI makes move after player"""
        game = self.client.post('/game/')
        game_id = game.data['id']
        payload = {'row': 8, 'col': 7}
        res = self.client.put(
            f'/game/{game_id}/',
            data=payload,
            content_type='application/json'
        )

        numTwo = 0
        for row in res.data['grid']:
            for num in row:
                if num == 2:
                    numTwo += 1
        self.assertIn(1, res.data['grid'][8])
        self.assertEqual(numTwo, 2)
        self.assertEqual(res.data['status'], 'Playing')
        self.assertEqual(res.data['winner'], 0)


class GameFunctionalityTests(TestCase):

    def setUp(self):
        self.game = Game.objects.create()

    def test_AI_find_choices(self):
        """Test that AI has found proper choices"""
        choices = self.game.find_choices()
        expected_choices = [
            (6, 6),
            (6, 7),
            (6, 8),
            (7, 6),
            (7, 8),
            (8, 6),
            (8, 7),
            (8, 8)
        ]
        self.assertEqual(choices, expected_choices)

    def test_AI_find_choices_edge(self):
        """
            Test that AI has found proper choices
            in the edge of the board
        """
        self.game.make_move(row=0, col=0)
        choices = self.game.find_choices()
        expected_choices = [
            (0, 1),
            (1, 0),
            (1, 1),
            (6, 6),
            (6, 7),
            (6, 8),
            (7, 6),
            (7, 8),
            (8, 6),
            (8, 7),
            (8, 8)
        ]
        self.assertEqual(choices, expected_choices)

    def test_AI_add_new_choices(self):
        """
            Test that AI properly updates choices when using
            minimax algorithm to explore potential choices
        """
        choices = self.game.find_choices()
        self.game.make_move(row=7, col=6)
        move = (7, 6)
        additional_choices = self.game.add_new_choices(move, choices)
        expected_additional_choices = [
            (6, 5),
            (7, 5),
            (8, 5)
        ]
        self.assertEqual(additional_choices, expected_additional_choices)

    def test_AI_eval_grid_score(self):
        """Test that AI properly evaluates grid score"""
        movesets = [
            (8, 7),
            (8, 8),
            (8, 9)
        ]
        for move in movesets:
            self.game.make_ghost_move((move[0], move[1]), player_turn=1)
        score_straight_three = self.game.evaluate_board_score()
        self.game.make_ghost_move((8, 10), player_turn=2)
        score_three = self.game.evaluate_board_score()
        self.assertLess(score_straight_three, score_three)
