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
        if len(self.players) < 2:
            self.players.append({name: pin})
        if len(self.players) == 2:
            random.shuffle(self.players)
