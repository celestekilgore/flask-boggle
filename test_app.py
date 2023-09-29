from unittest import TestCase

from app import app, games

import json

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

            self.assertEqual(response.status_code,200)
            self.assertIn("<title>Boggle</title>",html)
            self.assertIn("Home Page Template",html)
            # test that you're getting a template


    def test_api_new_game(self):
        """Test starting a new game."""
        with app.test_client() as client:
            #FIXME: need to add POST data for response
            response = client.post('/api/new-game')
            game_data = response.get_json()


            breakpoint()
            print('response', response, 'html', game_data)

            self.assertEqual(type(game_data["board"]),list)
            #TODO: check that there is a list inside list
            self.assertEqual(type(game_data["gameId"]),str)
            #TODO: checl the route stores the new game in the games dictionary
            self.assertTrue(response.is_json)
            self.assertEqual(response.status_code,200)
            # write a test for this route
