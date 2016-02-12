import json


class MockSlackClient:
    def __init__(self):
        self.api_calls = []
        self.ts = 0
    
    def api_call(self, api_function, text=None, channel=None, ts=None, username=None, as_user=None, user=None):
        self.api_calls.append((api_function, text, channel, ts, username, as_user))
        if user:
            return json.dumps({'user': {'name': user}}).encode('utf-8')
        if "im.list" == api_function:
            return json.dumps({'ims': [{'user': 'p1', 'id':'p1_dm'},
                                       {'user': 'p2', 'id':'p2_dm'},
                                       {'user': 'p3', 'id':'p3_dm'},
                                       {'user': 'p4', 'id':'p4_dm'},
                                       {'user': 'p5', 'id':'p5_dm'}]}).encode('utf-8')
        else:
            self.ts += 1
            return json.dumps({'ts':self.ts}).encode('utf-8')