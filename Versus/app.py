from flask import Flask, render_template, request, jsonify

from Versus.Classes import DefaultError, Game

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
    print(new_game_id, name, pin)
    if not (name and pin):
        raise DefaultError(message="Please provide a valid name and PIN combination.", status_code=401)
    if new_game_id is None:
        game = Game()
        game.add_player(name, pin)
        games.append(game)
        return game.game_id
    else:
        for game in games:
            if new_game_id == game.game_id:
                game.add_player(name, pin)
                break
            else:
                raise DefaultError(message="Please provide a valid game ID.", status_code=404)
        return "Game created successfully"


@app.route("/move", methods=["POST"])
def move():
    return "Made a move."


@app.route("/getCLIboard")
def get_CLI_board():
    return "Got CLI board."


if __name__ == '__main__':
    app.run(debug=True)
