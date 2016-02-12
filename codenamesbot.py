from slackclient import SlackClient
import os

from game import Game

token = os.environ["SLACK_TOKEN"]
slack_client = SlackClient(token)


outputs = []
crontable = [[1, "tick"]]
current_game = Game(slack_client)


def tick():
    current_game.tick()


def process_message(data):
    print(data)

    if data['type'] == 'message' and 'text' in data:
        current_game.process(data)














