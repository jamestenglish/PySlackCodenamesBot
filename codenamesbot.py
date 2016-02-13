from slackclient import SlackClient
import os
import json

from game import Game

token = os.environ["SLACK_TOKEN"]
bot_name = os.environ["BOT_NAME"]
slack_client = SlackClient(token)


outputs = []
crontable = [[1, "tick"]]
result = slack_client.api_call('users.list')
bot_user_id = None

if result:
    result = result.decode("utf-8")
    result = json.loads(result)

    for member in result['members']:
        if member['name'].lower() == bot_name.lower():
            bot_user_id = member['id']

current_game = Game(slack_client)

def tick():
    current_game.tick()

def process_message(data):

    if data['type'] == 'message' and 'text' in data and data['user'] != bot_user_id:
        current_game.process(data)














