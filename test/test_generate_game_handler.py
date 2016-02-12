import unittest

from test.mock_slack_client import MockSlackClient
from game_state import GameState
from generate_game_handler import GenerateGameHandler
from clue_input_handler import ClueInputHandler
from player import Player
from test.random_mock import RandomMock


class MockChat:
    def __init__(self):
        self.messages = []
        
    def message(self, message, other=None):
        self.messages.append(message)

class TestGenerateGameHandler(unittest.TestCase):
    

    def _add_players(self, slack_client, game_state):
        manager = game_state.team_manager
        manager.add_player(Player("p1", slack_client))
        manager.add_player(Player("p2", slack_client))
        manager.add_player(Player("p3", slack_client))
        manager.add_player(Player("p4", slack_client))
        manager.add_player(Player("p5", slack_client))

    def test_tick(self):
        
        random = RandomMock()
        slack_client = MockSlackClient()
        game_state = GameState(slack_client, random_func=random, chat=MockChat())
        handler = GenerateGameHandler(game_state)
        
        self._add_players(slack_client, game_state)
        
        handler.tick()
        
        self.assertTrue(isinstance(game_state.handler, ClueInputHandler))
        
        self.assertEqual("p1_dm", slack_client.api_calls[-1][2])
        self.assertEqual("p3_dm", slack_client.api_calls[-2][2])
