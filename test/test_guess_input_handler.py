import unittest
from test.random_mock import RandomMock
from test.mock_slack_client import MockSlackClient
from game_state import GameState
from player import Player
from chat import Chat
from guess_input_handler import GuessInputHandler
from game_end_exception import GameEndException
from board import BLUE_TEAM, RED_TEAM
from clue_input_handler import ClueInputHandler


class TestGuessInputHandler(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        random = RandomMock()
        self.slack_client = MockSlackClient()
        self.game_state = GameState(self.slack_client,
                                    random_func=random,
                                    chat=Chat(self.slack_client, "chat_chanel"),
                                    channel="chat_chanel")
        self.handler = GuessInputHandler(self.game_state, 2)
        self._add_players(self.slack_client, self.game_state)
        
    def _add_players(self, slack_client, game_state):
        manager = game_state.team_manager
        manager.add_player(Player("p1", slack_client))  # red team
        manager.add_player(Player("p2", slack_client))
        manager.add_player(Player("p3", slack_client))  # blue team
        manager.add_player(Player("p4", slack_client))
        manager.add_player(Player("p5", slack_client))
        manager.pick_teams()
    
    def test_is_guess_command(self):
        data = {'text': 'cn guess foo', 'channel': 'chat_chanel'}
        self.assertTrue(self.handler._is_guess_command(data))
        
        data = {'text': 'cn gUess foo', 'channel': 'chat_chanel'}
        self.assertTrue(self.handler._is_guess_command(data))
        
        data = {'text': 'cn stop guess', 'channel': 'chat_chanel'}
        self.assertTrue(self.handler._is_guess_command(data))
        
    def test_is_guess_command_fail(self):
        data = {'text': 'cn guess foo', 'channel': 'foo'}
        self.assertFalse(self.handler._is_guess_command(data))
        
        data = {'text': 'guess foo', 'channel': 'chat_chanel'}
        self.assertFalse(self.handler._is_guess_command(data))
        
    def test_is_current_player(self):
        data = {'text': 'cn guess foo', 'channel': 'chat_chanel', 'user': 'p4'}
        self.assertTrue(self.handler._is_current_player(data))
        
    def test_is_current_player_fail(self):
        data = {'text': 'cn guess foo', 'channel': 'chat_chanel', 'user': 'p3'}
        self.assertFalse(self.handler._is_current_player(data))
        
        data = {'text': 'cn guess foo', 'channel': 'chat_chanel', 'user': 'p2'}
        self.assertFalse(self.handler._is_current_player(data))
        
        data = {'text': 'cn guess foo', 'channel': 'chat_chanel', 'user': 'p1'}
        self.assertFalse(self.handler._is_current_player(data))
        
    def test_process_guess_fail(self):
        data = {'text': 'cn guess foo', 'channel': 'chat_chanel', 'user': 'p4'}
        self.handler.process(data)
        self.assertEqual("Invalid Guess, not a choice on the board! Try again", self.slack_client.api_calls[-1][1])
        
        data = {'text': 'cn guess foo', 'channel': 'chat_chanel', 'user': 'p1'}
        self.handler.process(data)
        self.assertEqual("Shush <@p1>! It's not your turn to guess!", self.slack_client.api_calls[-1][1])

    def test_process_stop_fail(self):
        data = {'text': 'cn stop guess', 'channel': 'chat_chanel', 'user': 'p4'}
        self.handler.process(data)
        self.assertEqual("You have to guess at least once!", self.slack_client.api_calls[-1][1])
        
    def test_handle_assassin_guess(self):
        exception_occurred = False
        try: 
            self.handler._handle_assassin_guess('bear')
        except GameEndException:
            exception_occurred = True
            
        self.assertTrue(exception_occurred)
        self.assertEqual("You picked the assassin! Blue Team loses! Red Team wins!", self.slack_client.api_calls[-1][1])

    def test_process_valid_guess_incorrect_assassin(self):
        data = {'text': 'cn guess bear', 'channel': 'chat_chanel', 'user': 'p4'}
        exception_occured = False
        try: 
            self.handler.process(data)
        except GameEndException:
            exception_occured = True
            
        self.assertTrue(exception_occured)
        self.assertEqual("You picked the assassin! Blue Team loses! Red Team wins!", self.slack_client.api_calls[-1][1])
        
    def test_is_wrong_guess(self):
        self.assertTrue(self.handler._is_wrong_guess('AFRICA', BLUE_TEAM))
        self.assertTrue(self.handler._is_wrong_guess('AFRICA', RED_TEAM))
        
        self.assertFalse(self.handler._is_wrong_guess('AMERICA', RED_TEAM))
        self.assertTrue(self.handler._is_wrong_guess('AMERICA', BLUE_TEAM))
        
        self.assertTrue(self.handler._is_wrong_guess('BEACH', RED_TEAM))
        self.assertFalse(self.handler._is_wrong_guess('BEACH', BLUE_TEAM))

    def test_process_wrong_guess(self):
        data = {'text': 'cn guess angel', 'channel': 'chat_chanel', 'user': 'p4'}
        self.handler.process(data)
        self.assertEqual("Wrong answer! On to the Red Team", self.slack_client.api_calls[-1][1])
        self.assertTrue(isinstance(self.game_state.handler, ClueInputHandler))
        
    def test_process_valid_guess_correct_last_guess(self):
        
        data = {'text': 'cn guess back', 'channel': 'chat_chanel', 'user': 'p4'}
        self.handler.process(data)
        
        data = {'text': 'cn guess ball', 'channel': 'chat_chanel', 'user': 'p4'}
        self.handler.process(data)
        
        data = {'text': 'cn guess band', 'channel': 'chat_chanel', 'user': 'p4'}
        self.handler.process(data)
        
        self.assertEqual("No more guesses! On to the Red Team", self.slack_client.api_calls[-1][1])
        self.assertTrue(isinstance(self.game_state.handler, ClueInputHandler))

    def test_process_valid_guess_correct(self):
        data = {'text': 'cn guess back', 'channel': 'chat_chanel', 'user': 'p4'}
        self.handler.process(data)
        self.assertEqual("Correct! You have 2 more guesses.", self.slack_client.api_calls[-2][1])

    def test_get_winner(self):
        board = self.handler.board
        board.update_board_reveal_secret('AMERICA')
        self.assertEqual(None, board.get_winner())

        board.update_board_reveal_secret('ANGEL')
        self.assertEqual(None, board.get_winner())

        board.update_board_reveal_secret('ANTARCTICA')
        self.assertEqual(None, board.get_winner())

        board.update_board_reveal_secret('APPLE')
        self.assertEqual(None, board.get_winner())

        board.update_board_reveal_secret('ARM')
        self.assertEqual(None, board.get_winner())

        board.update_board_reveal_secret('ATLANTIS')
        self.assertEqual(None, board.get_winner())

        board.update_board_reveal_secret('AUSTRALIA')
        self.assertEqual(None, board.get_winner())

        board.update_board_reveal_secret('AZTEC')
        self.assertEqual(RED_TEAM, board.get_winner())

    def test_handle_if_win(self):
        board = self.handler.board
        board.update_board_reveal_secret('AMERICA')
        board.update_board_reveal_secret('ANGEL')
        board.update_board_reveal_secret('ANTARCTICA')
        board.update_board_reveal_secret('APPLE')
        board.update_board_reveal_secret('ARM')
        board.update_board_reveal_secret('ATLANTIS')
        board.update_board_reveal_secret('AUSTRALIA')
        board.update_board_reveal_secret('AZTEC')

        exception_occurred = False
        try:
            self.handler._handle_if_win()
        except GameEndException:
            exception_occurred = True

        self.assertTrue(exception_occurred)

    def test_process_valid_guess_correct_win(self):
        self.handler.max_guess_count = 999

        data = {'text': 'cn guess BACK', 'channel': 'chat_chanel', 'user': 'p4'}
        self.handler.process(data)

        data = {'text': 'cn guess BALL', 'channel': 'chat_chanel', 'user': 'p4'}
        self.handler.process(data)

        data = {'text': 'cn guess BAND', 'channel': 'chat_chanel', 'user': 'p4'}
        self.handler.process(data)

        data = {'text': 'cn guess BANK', 'channel': 'chat_chanel', 'user': 'p4'}
        self.handler.process(data)

        data = {'text': 'cn guess BAR', 'channel': 'chat_chanel', 'user': 'p4'}
        self.handler.process(data)

        data = {'text': 'cn guess BARK', 'channel': 'chat_chanel', 'user': 'p4'}
        self.handler.process(data)

        data = {'text': 'cn guess BAT', 'channel': 'chat_chanel', 'user': 'p4'}
        self.handler.process(data)

        data = {'text': 'cn guess BATTERY', 'channel': 'chat_chanel', 'user': 'p4'}
        self.handler.process(data)

        data = {'text': 'cn guess BEACH', 'channel': 'chat_chanel', 'user': 'p4'}

        exception_occurred = False
        try:
            self.handler.process(data)
        except GameEndException:
            exception_occurred = True

        self.assertTrue(exception_occurred)

    def test_process_stop(self):
        data = {'text': 'cn guess BATTERY', 'channel': 'chat_chanel', 'user': 'p4'}
        self.handler.process(data)

        data = {'text': 'cn stop guess', 'channel': 'chat_chanel', 'user': 'p4'}
        self.handler.process(data)
        self.assertEqual("Ok on to Red Team", self.slack_client.api_calls[-1][1])
