import json
import random
import uuid

import chess


class DefaultError(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class Game:

    def __init__(self):
        self.game_id = str(uuid.uuid4())[:8]
        self.players = []
        self.board = chess.Board()
        self.moves = 0

    def add_player(self, name, pin):
        if len(self.players) == 2:
            raise DefaultError("Game " + self.game_id + " is already full!", status_code=403)
        if len(self.players) == 1:
            self.players.append({name: pin})
            random.shuffle(self.players)
        if len(self.players) == 0:
            self.players.append({name: pin})

    def move(self, move, name, pin):
        if self.players[self.moves % 2] != {name: pin}:
            raise DefaultError("It's not your turn!", status_code=425)
        try:
            self.board.push(chess.Move.from_uci(move))
        except:
            raise DefaultError("Invalid move!", status_code=403)
        self.moves += 1
        print(self.board)


class PublicGame():
    def __init__(self, game: Game):
        self.game_id = game.game_id
        self.players = self.populate_players(game.players)
        # self.board = game.board
        self.moves = game.moves

    def populate_players(self, players):  # FIX
        pub_players = []
        for player in players:
            while len(pub_players) < 2:
                for name in player:
                    pub_players.append(name)
        return pub_players

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)
