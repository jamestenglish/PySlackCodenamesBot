import unittest
from .mock_slack_client import MockSlackClient
from game_state import GameState
from clue_input_handler import ClueInputHandler
from player import Player

from chat import Chat

from .random_mock import RandomMock


class TestClueInputHandler(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        random = RandomMock()
        self.slack_client = MockSlackClient()
        self.game_state = GameState(self.slack_client, random_func=random, chat=Chat(self.slack_client, "chat_chanel"))
        self.handler = ClueInputHandler(self.game_state)
        self._add_players(self.slack_client, self.game_state)
    
    def _add_players(self, slack_client, game_state):
        manager = game_state.team_manager
        manager.add_player(Player("p1", slack_client))  # red team
        manager.add_player(Player("p2", slack_client))
        manager.add_player(Player("p3", slack_client))  # blue team
        manager.add_player(Player("p4", slack_client))
        manager.add_player(Player("p5", slack_client))
        manager.pick_teams()
    
    def test_solict_word_tick(self):
        self.handler.tick()
        self.assertEqual(self.handler.tick_func, None)
        
        self.assertEqual("p3_dm", self.slack_client.api_calls[-1][2])
        self.assertEqual("What is your one word clue?", self.slack_client.api_calls[-1][1])
        
    def test_process_word_fail(self):
        self.handler.tick()
        self.handler.process({"text": "foo bar", "channel": "p3_dm"})
        self.assertEqual("Invalid input! One word only! Please try again...", self.slack_client.api_calls[-1][1])
        self.assertEqual("p3_dm", self.slack_client.api_calls[-1][2])
        
        self.handler.process({"text": "foo bar", "channel": "p3_dm"})
        self.assertEqual("Invalid input! One word only! Please try again...", self.slack_client.api_calls[-3][1])
        self.assertEqual("Invalid input! One word only! Please try again...", self.slack_client.api_calls[-1][1])

    def test_process_word(self):
        self.handler.tick()
        self.handler.process({"text": "foo", "channel": "p3_dm"})
        self.assertEqual("foo", self.handler.clue_word)  
        self.assertEqual("What is your clue number? [0-999]", self.slack_client.api_calls[-1][1])
        self.assertEqual("p3_dm", self.slack_client.api_calls[-1][2])
        
    def test_process_number_fail(self):
        self.handler.tick()
        self.handler.process({"text": "foo", "channel": "p3_dm"})
        self.handler.process({"text": "bar", "channel": "p3_dm"})
        self.assertEqual("Invalid Input! Enter a number [0-999]", self.slack_client.api_calls[-1][1])
        self.assertEqual("p3_dm", self.slack_client.api_calls[-1][2])
        
        self.handler.process({"text": "bar", "channel": "p3_dm"})
        self.assertEqual("Invalid Input! Enter a number [0-999]", self.slack_client.api_calls[-3][1])
        self.assertEqual("Invalid Input! Enter a number [0-999]", self.slack_client.api_calls[-1][1])
        self.assertEqual("p3_dm", self.slack_client.api_calls[-1][2])
        
    def test_process_number(self):
        self.handler.tick()
        self.handler.process({"text": "foo", "channel": "p3_dm"})
        self.handler.process({"text": "12", "channel": "p3_dm"})
        
        self.assertEqual(12, self.game_state.clue_number)
        self.assertEqual("*Blue Team:* your clue is: `foo 12`", self.slack_client.api_calls[-2][1])
  

        
        