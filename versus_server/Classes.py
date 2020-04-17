import random
import uuid


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
    game_id = str(uuid.uuid4())[:8]
    players = []

    def add_player(self, name, pin):
        if len(self.players) == 2:
            raise DefaultError("Game " + self.game_id + " is already full!")
        if len(self.players) == 1:
            self.players.append({name, pin})
            random.shuffle(self.players)
        if len(self.players) == 0:
            self.players.append({name: pin})
