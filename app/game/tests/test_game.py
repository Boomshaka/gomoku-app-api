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
        payload = {'row': 7, 'col': 7}
        res = self.client.put(
            f'/game/{game_id}/',
            data=payload,
            content_type='application/json'
        )
        self.assertContains(res, game_id, count=1, status_code=200)
        self.assertIn(1, res.data['grid'][7])
        self.assertEquals(res.data['status'], 'Playing')
        self.assertEquals(res.data['winner'], 0)

    def test_invalid_index_col(self):
        """Test that invalid col index returns an index error"""
        game = self.client.post('/game/')
        game_id = game.data['id']
        payload = {'row': 0, 'col': -1}
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
        payload = {'row': -1, 'col': 0}
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
        payload = {'row': 0, 'col': 0}
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
            {'row': 0, 'col': 0},
            {'row': 0, 'col': 1},
            {'row': 0, 'col': 2},
            {'row': 0, 'col': 3},
            {'row': 0, 'col': 4}
        ]
        res = None
        for p in payload:
            res = self.client.put(
                f'/game/{game_id}/',
                data=p,
                content_type='application/json'
            )
        self.assertEqual(res.status_code, 200)
        self.assertEquals(res.data['status'], 'Finished')
        self.assertNotEqual(res.data['winner'], 0)

    def test_winner_row(self):
        """Test for winner when there's horizontal 5"""
        game = self.client.post('/game/')
        game_id = game.data['id']
        payload = [
            {'row': 0, 'col': 0},
            {'row': 1, 'col': 0},
            {'row': 2, 'col': 0},
            {'row': 3, 'col': 0},
            {'row': 4, 'col': 0}
        ]
        res = None
        for p in payload:
            res = self.client.put(
                f'/game/{game_id}/',
                data=p,
                content_type='application/json'
            )
        self.assertEqual(res.status_code, 200)
        self.assertEquals(res.data['status'], 'Finished')
        self.assertNotEqual(res.data['winner'], 0)

    def test_winner_diagonal(self):
        """Test for winner when there's diagonal 5"""
        game = self.client.post('/game/')
        game_id = game.data['id']
        payload = [
            {'row': 0, 'col': 0},
            {'row': 1, 'col': 1},
            {'row': 2, 'col': 2},
            {'row': 3, 'col': 3},
            {'row': 4, 'col': 4}
        ]
        res = None
        for p in payload:
            res = self.client.put(
                f'/game/{game_id}/',
                data=p,
                content_type='application/json'
            )
        self.assertEqual(res.status_code, 200)
        self.assertEquals(res.data['status'], 'Finished')
        self.assertNotEqual(res.data['winner'], 0)
