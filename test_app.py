from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with app.test_client() as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("<title>Boggle</title>", html)
            self.assertIn("Home Page Template", html)
            # test that you're getting a template

    def test_api_new_game(self):
        """Test starting a new game."""

        with app.test_client() as client:
            response = client.post('/api/new-game')
            game_data = response.get_json()

            self.assertEqual(type(game_data["board"]), list)
            self.assertEqual(type(game_data["board"][0]), list)
            self.assertEqual(type(game_data["gameId"]), str)
            self.assertIn(game_data['gameId'], games)
            self.assertTrue(response.is_json)
            self.assertEqual(response.status_code, 200)

    def test_api_score_word_json(self):
        """Test scoring a word."""
        with app.test_client() as client:

            game_response = client.post('/api/new-game')
            game_data = game_response.get_json()
            test_game_id = game_data["gameId"]

            games[test_game_id].board = (
                ["C", "A", "T"],
                ["O", "X", "X"],
                ["X", "G", "X"]
            )

            # testing invalid word
            response = client.post(
                '/api/score-word',
                json={
                    'gameId': test_game_id,
                    'word': "cat"
                }
            )

            invalid_word_data = response.get_json()
            self.assertEqual(invalid_word_data, {"result": "not-word"})

            # test not-on-board word
            response = client.post(
                '/api/score-word',
                json={
                    'gameId': test_game_id,
                    'word': "DOG"
                }
            )
            
            off_board_word_data = response.get_json()
            self.assertEqual(off_board_word_data, {"result": "not-on-board"})

            # testing valid word
            response = client.post('/api/score-word',
                                   json={'gameId': test_game_id, 'word': "CAT"})
            valid_word_data = response.get_json()
            self.assertEqual(valid_word_data, {"result": "ok"})
