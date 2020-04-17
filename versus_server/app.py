from flask import Flask, render_template, request, jsonify

from versus_server.Classes import DefaultError, Game, PublicGame

app = Flask(__name__)
games = []


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
    move = request.args.get("move")
    name = request.args.get("name")
    pin = request.args.get("pin")
    for game in games:
        if game.game_id == game_id:
            game.move(move, name, pin)
            return str(0)
    raise DefaultError("Game not found!", status_code=404)


@app.route("/getCLIboard")
def get_CLI_board():
    return "Got CLI board."


@app.route("/games")
def get_games():
    pub_games = []
    for game in games:
        pub_games.append(PublicGame(game).toJSON())
    return jsonify(pub_games)


if __name__ == '__main__':
    app.run(debug=True)
