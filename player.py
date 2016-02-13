import json
from chat import Chat


class Player:

    def __init__(self, slack_id, slack_client):
        self.slack_id = slack_id
        self.slack_client = slack_client
        self.chat = Chat(slack_client, self.get_im_channel())

    def get_im_channel(self):
        result = self.slack_client.api_call('im.list')
        if result:
            result = result.decode("utf-8")
        ims = json.loads(result)['ims']
        for im in ims:
            if im['user'] == self.slack_id:
                return im['id']

        raise Exception("IM Channel not found!")

    def get_username(self):
        result = self.slack_client.api_call('users.info', user=self.slack_id)
        if result:
            result = result.decode("utf-8")

        user_api = json.loads(result)['user']
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