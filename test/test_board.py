import unittest
from board import BLUE_TEAM, Board
from wordlist import word_list
from .random_mock import RandomMock

class ChatMock:
    pass
            

class TestBoard(unittest.TestCase):
    
    def test_init(self):
        chat = ChatMock()
        random = RandomMock()
        board = Board(chat, random)
        self.assertEqual(word_list[:25], board.current_board)
        self.assertEqual(BLUE_TEAM, board.current_team)
        secret_board = [':white_circle:', ':white_circle:', ':white_circle:', ':white_circle:', ':white_circle:', ':white_circle:', ':white_circle:',
                        ':red_circle:', ':red_circle:', ':red_circle:', ':red_circle:', ':red_circle:', ':red_circle:',':red_circle:',':red_circle:',
                        ':large_blue_circle:', ':large_blue_circle:', ':large_blue_circle:', ':large_blue_circle:', ':large_blue_circle:', ':large_blue_circle:', ':large_blue_circle:', ':large_blue_circle:', ':large_blue_circle:',
                        ':black_circle:']
        self.assertEqual(25, len(board.secret_board))
        self.assertEqual(secret_board, board.secret_board)
        
        board_string = "AFRICA      | AGENT       | AIR         | ALIEN       | ALPS        | \nAMAZON      | AMBULANCE   | AMERICA     | ANGEL       | ANTARCTICA  | \nAPPLE       | ARM         | ATLANTIS    | AUSTRALIA   | AZTEC       | \nBACK        | BALL        | BAND        | BANK        | BAR         | \nBARK        | BAT         | BATTERY     | BEACH       | BEAR        | \n"
        self.assertEqual(board_string, board._get_current_board_string())
        
        board_string = ":white_circle: | :white_circle: | :white_circle: | :white_circle: | :white_circle: | \n:white_circle: | :white_circle: | :red_circle: | :red_circle: | :red_circle: | \n:red_circle: | :red_circle: | :red_circle: | :red_circle: | :red_circle: | \n:large_blue_circle: | :large_blue_circle: | :large_blue_circle: | :large_blue_circle: | :large_blue_circle: | \n:large_blue_circle: | :large_blue_circle: | :large_blue_circle: | :large_blue_circle: | :black_circle: | \n"
        self.assertEqual(board_string, board._get_secret_board_string())
