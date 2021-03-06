import json


class Chat:
    def __init__(self, slack_client, channel):
        self.slack_client = slack_client
        self.channel = channel

    def message(self, text, last_message=None):
        result = None
        if last_message:
            result = self.slack_client.api_call('chat.update',
                                                text=text,
                                                channel=self.channel,
                                                ts=last_message['ts'])
        else:
            result = self.slack_client.api_call('chat.postMessage',
                                                text=text,
                                                channel=self.channel,
                                                username='omnibot',
                                                as_user=True)

        if result:
            result = result.decode("utf-8")
        else:
            return result
        result = json.loads(result)

        return(result)
