import chess
import chess.svg
from flask import Flask, render_template, request, jsonify
from markupsafe import Markup

from versus_server.Classes import DefaultError, Game, PublicGame

app = Flask(__name__, template_folder='templates')
games = []


def find_game(game_id) -> Game:
    for game in games:
        if game.game_id == game_id:
            return game


@app.errorhandler(DefaultError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/newgame")
def new_game():
    new_game_id = request.args.get("id")
    name = request.args.get("name")
    pin = request.args.get("pin")
    if not (name and pin):
        raise DefaultError(message="Please provide a valid name and PIN combination.", status_code=401)
    if new_game_id is None:
        game = Game()
        game.add_player(name, pin)
        games.append(game)
        return game.game_id
    else:
        if len(games) == 0:
            raise DefaultError(message="Please provide a valid game ID.", status_code=404)
        for game in games:
            if new_game_id == game.game_id:
                game.add_player(name, pin)
                break
            else:
                raise DefaultError(message="Please provide a valid game ID.", status_code=404)
        return str(0)


@app.route("/move")
def move():
    game_id = request.args.get("id")
    move_to_make = request.args.get("move")
    name = request.args.get("name")
    pin = request.args.get("pin")
    game = find_game(game_id)
    if game is None:
        raise DefaultError("Game not found!", status_code=404)
    return game.move(move_to_make, name, pin)


@app.route("/getboard")
def get_board():
    game_id = request.args.get("id")
    game = find_game(game_id)
    if not game:
        raise DefaultError(message="Waiting for all players to join...", status_code=425)
    if len(game.players) < 2:
        raise DefaultError(message="Waiting for all players to join...", status_code=425)
    svg = chess.svg.board(board=game.board, size=800)
    return render_template("board.html", svg=Markup(svg), id=game_id, name1=game.players[0].name,
                           name2=game.players[1].name)


@app.route("/games")
def get_games():
    ret_games = []
    for game in games:
        ret_games.append(PublicGame(game).to_json())
    return jsonify(ret_games)


if __name__ == '__main__':
    app.run(port="80")
