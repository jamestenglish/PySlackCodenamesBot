import unittest
from test.random_mock import RandomMock
from test.mock_slack_client import MockSlackClient
from game_state import GameState
from chat import Chat
from resolve_invalid_handler import ResolveInvalidHandler
from player import Player
from clue_input_handler import ClueInputHandler


class TestResolveInvalidHandler(unittest.TestCase):

    def setUp(self):
        random = RandomMock()
        self.slack_client = MockSlackClient()
        self.game_state = GameState(self.slack_client,
                                    random_func=random,
                                    chat=Chat(self.slack_client, "chat_chanel"),
                                    channel="chat_chanel")

        self.handler = ResolveInvalidHandler(self.game_state)
        self._add_players(self.slack_client, self.game_state)

    def _add_players(self, slack_client, game_state):
        manager = game_state.team_manager
        manager.add_player(Player("p1", slack_client))  # red team
        manager.add_player(Player("p2", slack_client))
        manager.add_player(Player("p3", slack_client))  # blue team
        manager.add_player(Player("p4", slack_client))
        manager.add_player(Player("p5", slack_client))
        manager.pick_teams()

    def test_invalid_word(self):
        data = {"text": "foo", "channel": "p3_dm"}
        self.handler.process(data)
        self.assertEqual("Invalid! Please try again...", self.slack_client.api_calls[-1][1])

    def test_process(self):
        data = {"text": "band", "channel": "p3_dm"}
        self.handler.process(data)
        self.assertEqual("Still Blue Team's turn. Getting next clue...", self.slack_client.api_calls[-1][1])
        self.assertTrue(isinstance(self.game_state.handler, ClueInputHandler))
