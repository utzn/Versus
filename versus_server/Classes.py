import json
import random
import uuid
from enum import Enum

import chess


class Response:
    def __init__(self, id, message):
        self.id = id
        self.message = message

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)


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
        self.moves = []
        self.board = chess.Board()
        self.game_state = GameState.INITIAL_POS

    def add_player(self, name, pin) -> None:
        if len(self.players) == 2:
            raise DefaultError("Game " + self.game_id + " is already full.", status_code=403)
        if len(self.players) == 1:
            self.players.append(Player(name, pin))
            random.shuffle(self.players)
        if len(self.players) == 0:
            self.players.append(Player(name, pin))

    def move(self, move, name, pin) -> str:
        if self.game_state != GameState.INITIAL_POS and self.game_state != GameState.IN_PROGRESS:
            raise DefaultError("Game is already over.", status_code=403)
        else:
            if self.players[len(self.moves) % 2].name != name or self.players[len(self.moves) % 2].pin != pin:
                raise DefaultError("It's not your turn (wrong name/pin combination).", status_code=425)
            if chess.Move.from_uci(move) in self.board.legal_moves:
                if self.game_state is GameState.INITIAL_POS:
                    self.game_state = GameState.IN_PROGRESS
                try:
                    self.board.push(chess.Move.from_uci(move))
                    self.moves.append(move)
                    self.no_of_moves += 1
                    if self.board.is_checkmate():
                        if len(self.moves) % 2 == 0:
                            self.game_state = GameState.WHITE_MATE
                        else:
                            self.game_state = GameState.BLACK_MATE
                        return str(chess.Move.from_uci(move)) + "#"
                    if self.board.is_check():
                        if len(self.moves) % 2 == 0:
                            self.game_state = GameState.WHITE_CHECK
                        else:
                            self.game_state = GameState.BLACK_CHECK
                        return str(chess.Move.from_uci(move)) + "+"
                    if self.board.is_variant_draw():
                        self.game_state = GameState.DRAW
                        return str(chess.Move.from_uci(move)) + "="
                    return str(chess.Move.from_uci(move))
                except:
                    raise DefaultError("Can't move a piece from this square.", status_code=403)

            else:
                raise DefaultError("Illegal move.", status_code=403)


class GameState(Enum):
    INITIAL_POS = 1
    IN_PROGRESS = 2
    WHITE_CHECK = 3
    BLACK_CHECK = 4
    WHITE_MATE = 5
    BLACK_MATE = 6
    DRAW = 7

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)


class PlayerState(Enum):
    PLAYING = 1
    WON = 2
    LOST = 3


class Player:
    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
        self.player_state = PlayerState.PLAYING


class PublicGame:
    def __init__(self, game: Game, include_id=True):
        if include_id:
            self.game_id = game.game_id
        self.players = self.populate_players(game.players)
        # self.board = game.board
        self.game_state = str(game.game_state.name)
        self.moves = game.moves

    @staticmethod
    def populate_players(players) -> []:
        pub_players = []
        for player in players:
            pub_players.append(player.name)
        return pub_players
