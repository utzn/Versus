import argparse
import sys
import uuid

import chess
import chess.engine
import requests

parser = argparse.ArgumentParser(description="Simple Versus client")
parser.add_argument("-u", "--url",
                    help="URL or IP of the Versus instance",
                    default="http://localhost",
                    dest="url")
parser.add_argument("-n", "--name",
                    help="display name",
                    default="Default",
                    dest="name")
parser.add_argument("-c", "--computer",
                    help="Specify whether computer mode is enabled or not",
                    default="yes",
                    dest="computer")
parser.add_argument("-e", "--engine",
                    help="Path to the chess engine which should be moved for move generation, if --computer is set to yes",
                    default="stockfish_20011801_x64.exe",
                    dest="engine")

args = parser.parse_args()

if args.computer == "yes":
    human_mode = False
else:
    human_mode = True


def new_game():
    print("1    -   Create new game")
    print("2    -   Join existing game")
    local_game_id = None
    choice = int(input())
    if choice == 1:
        try:
            r = requests.get(url=args.url + "/newgame?name=" + args.name + "&pin=" + pin)
        except:
            print("Connection to " + args.url + " could not be established.")
            raise
        local_game_id = r.json()["id"]
        print(r.json()["message"] + " " + r.json()["id"])
        print("Waiting for all players to join...")
    if choice == 2:
        print("Please enter game ID:")
        local_game_id = str(input())
        try:
            r = requests.get(
                url=args.url + "/newgame?id=" + local_game_id + "&name=" + args.name + "&pin=" + pin)
            response = r.json()
            print(response["message"] + " " + response["id"])
        except:
            print("Connection to " + args.url + " could not be established.")
            raise
    return local_game_id


def calculate_move():
    engine = chess.engine.SimpleEngine.popen_uci(args.engine)
    r = requests.get(
        url=args.url + "/getfen?id=" + game_id)
    response = r.json()["fen"]
    board = chess.Board(response)
    while not board.is_game_over():
        result = engine.play(board, chess.engine.Limit(time=0.1))
        return str(result.move)


def move():
    if human_mode:
        print("Enter a move in UCI notation:")
        choice = str(input())
    else:
        choice = calculate_move()
        print("Engine made move " + choice)
    r = requests.get(url=args.url + "/move?id=" + game_id + "&move=" + choice + "&name=" + args.name + "&pin=" + pin)
    if r.status_code != 200:
        print(r.json()["message"])
    print("Waiting for other player...")


def game_is_active():
    r = requests.get(url=args.url + "/games?&id=" + game_id)
    if r.json()["game_state"] != "FINISHED":
        return True
    return False


def game_is_full():
    r = requests.get(url=args.url + "/games?&id=" + game_id)
    response = r.json()
    if len(response["players"]) == 2:
        return True
    return False


def is_my_turn():
    r = requests.get(url=args.url + "/games?&id=" + game_id)
    response = r.json()
    for idx, player in enumerate(response["players"]):
        if player == args.name:
            turn = idx % 2
            return len(response["moves"]) % 2 == turn


def is_player_human():
    print("Who is going to provide UCI moves for the upcoming game?")
    print("1    -   Machine")
    print("2    -   Human")
    choice = input()
    if choice == 1:
        return False
    else:
        return True


pin = str(uuid.uuid4())
try:
    game_id = new_game()
except:
    sys.exit(-1)

while not game_is_full():
    pass

while True:
    if is_my_turn():
        move()
