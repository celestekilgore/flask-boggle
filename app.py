from flask import Flask, request, render_template, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

debug = DebugToolbarExtension(app)

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    return jsonify(gameId=game_id, board=game.board)


@app.post("/api/score-word")
def word_score():
    """Take JSON containing word and gameId. Checks if word is valid (in word
    list and on the board). Plays and scores word if it is valid. Returns JSON:
    {result: 'not-word'} OR
    {result: 'not-on-board'} OR
    {result: 'ok'}
    """

    gameId = request.json['gameId']
    word = request.json['word']

    if not games[gameId].is_word_in_word_list(word):
        return jsonify(result='not-word')
    elif not games[gameId].check_word_on_board(word):
        return jsonify(result='not-on-board')
    else:
        games[gameId].play_and_score_word(word)
        return jsonify(result='ok')
