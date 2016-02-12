import json
from chat import Chat


class Player:

    def __init__(self, slack_id, slack_client):
        self.slack_id = slack_id
        self.slack_client = slack_client
        self.chat = Chat(slack_client, self.get_im_channel())

    def get_im_channel(self):
        ims = json.loads(self.slack_client.api_call('im.list'))['ims']
        for im in ims:
            if im['user'] == self.slack_id:
                return im['id']

        print(str(ims))
        raise "IM Channel not found!"

    def get_username(self):
        user_api = json.loads(self.slack_client.api_call('users.info', user=self.slack_id))['user']
        return user_api['name']

    def __hash__(self):
        return hash(self.slack_id)

    def __eq__(self, other):
        try:
            return hash(self) == hash(other)
        except:
            return False

    def __str__(self):
        return self.get_username()