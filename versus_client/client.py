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
    while True:
        print("1    -   Create new game")
        print("2    -   Join existing game")
        choice = int(input())
        if choice == 1:
            r = requests.get(url=args.url + "/newgame?name=" + args.name + "&pin=" + str(uuid.uuid4()))
            game_id = r.json()["id"]
            print(r.json()["message"] + r.json()["id"])
            break
        if choice == 2:
            print("Please enter game ID:")
            game_id = str(input())
            r = requests.get(
                url=args.url + "/newgame?id=" + game_id + "&name=" + args.name + "&pin=" + str(uuid.uuid4()))
            print(r.json()["message"] + r.json()["id"])
            break
        print("Please enter 1 or 2.")


new_game()
