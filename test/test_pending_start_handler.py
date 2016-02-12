import unittest
from game_state import GameState
from pending_start_handler import PendingStartHandler, START_COMMAND, JOIN_COMMAND
from .mock_slack_client import MockSlackClient
from game_end_exception import GameEndException
from generate_game_handler import GenerateGameHandler

class TestPendingStartHandler(unittest.TestCase):
    def setUp(self):
        self.slack_client = MockSlackClient()
        self.game_state = GameState(self.slack_client)
        self.handler = PendingStartHandler(self.game_state)
        
    def _start(self):
        data = {'text': START_COMMAND, 'channel': 'foo'}
        self.handler.process(data)
        
    def test_start(self):
        self._start()
        self.assertEquals('foo', self.game_state.channel)
        
    def test_players_join_success(self):
        self._start()
        data = {'text': JOIN_COMMAND, 'channel': 'foo', 'user': 'p1'}
        self.handler.process(data)
        
        data = {'text': JOIN_COMMAND, 'channel': 'foo', 'user': 'p2'}
        self.handler.process(data)
        
        data = {'text': JOIN_COMMAND, 'channel': 'foo', 'user': 'p3'}
        self.handler.process(data)
        
        data = {'text': JOIN_COMMAND, 'channel': 'foo', 'user': 'p4'}
        self.handler.process(data)
        
        self.assertEqual(4, len(self.game_state.team_manager.players))
        last_api_call = self.slack_client.api_calls[-1]
        self.assertEquals("You have joined the game!", last_api_call[1])
        
    def _count_down(self):
        self.handler.tick()
        last_api_call = self.slack_client.api_calls[-1]
        self.assertEquals("Starting Codenames game in 30 seconds. Reply `cn join` to play", last_api_call[1])
        self.handler.tick()
        self.handler.tick()
        self.handler.tick()
        self.handler.tick()
        self.handler.tick()
        self.handler.tick()
        self.handler.tick()
        self.handler.tick()
        self.handler.tick()
        self.handler.tick()
        self.handler.tick()
        self.handler.tick()
        self.handler.tick()
        self.handler.tick()
        self.handler.tick()
        self.handler.tick()
        self.handler.tick()
        self.handler.tick()
        self.handler.tick()
        self.handler.tick()
        self.handler.tick()
        self.handler.tick()
        self.handler.tick()
        self.handler.tick()
        self.handler.tick()
        self.handler.tick()
        self.handler.tick()
        self.handler.tick()
        self.handler.tick()

    def test_players_join_fail(self):
        self._start()
        data = {'text': JOIN_COMMAND, 'channel': 'foo', 'user': 'p1'}
        self.handler.process(data)
        
        data = {'text': JOIN_COMMAND, 'channel': 'foo', 'user': 'p2'}
        self.handler.process(data)
        
        data = {'text': JOIN_COMMAND, 'channel': 'foo', 'user': 'p3'}
        self.handler.process(data)
        
        self._count_down()
        
        last_api_call = self.slack_client.api_calls[-1]
        self.assertEquals("Starting Codenames game in 1 seconds. Reply `cn join` to play", last_api_call[1])
        
        caught_exception = False
        try:
            self.handler.tick()
        except GameEndException:
            caught_exception = True
            
        self.assertTrue(caught_exception)
        
    def test_players_join_success_start(self):
        self._start()
        data = {'text': JOIN_COMMAND, 'channel': 'foo', 'user': 'p1'}
        self.handler.process(data)
        
        data = {'text': JOIN_COMMAND, 'channel': 'foo', 'user': 'p2'}
        self.handler.process(data)
        
        data = {'text': JOIN_COMMAND, 'channel': 'foo', 'user': 'p3'}
        self.handler.process(data)
        
        data = {'text': JOIN_COMMAND, 'channel': 'foo', 'user': 'p4'}
        self.handler.process(data)
        
        self._count_down()
        self.handler.tick()
        
        self.assertTrue(isinstance(self.game_state.handler, GenerateGameHandler))
        
        