import argparse
import uuid

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
args = parser.parse_args()


def new_game():
    print("1    -   Create new game")
    print("2    -   Join existing game")
    choice = int(input())
    if choice == 1:
        r = requests.get(url=args.url + "/newgame?name=" + args.name + "&pin=" + pin)
        local_game_id = r.json()["id"]
        print(r.json()["message"] + " " + r.json()["id"])
        print("Waiting for all players to join...")
        return local_game_id
    if choice == 2:
        print("Please enter game ID:")
        local_game_id = str(input())
        r = requests.get(
            url=args.url + "/newgame?id=" + local_game_id + "&name=" + args.name + "&pin=" + pin)
        response = r.json()
        print(response["message"] + " " + response["id"])
        return local_game_id
    print("Please enter 1 or 2.")


def move():
    print("Enter a move in UCI notation:")
    choice = str(input())
    r = requests.get(url=args.url + "/move?id=" + game_id + "&move=" + choice + "name=" + args.name + "&pin=" + pin)
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


pin = str(uuid.uuid4())
game_id = new_game()
while not game_is_full():
    pass

while True:
    if is_my_turn():
        move()
