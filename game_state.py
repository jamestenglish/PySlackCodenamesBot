from team_manager import TeamManager
from pending_start_handler import PendingStartHandler
from generate_game_handler import GenerateGameHandler
from clue_input_handler import ClueInputHandler
from guess_input_handler import GuessInputHandler
from board import Board
from resolve_invalid_handler import ResolveInvalidHandler
import random


class GameState:
    def __init__(self, slack_client, random_func=None, chat=None, channel=None):
        self.chat = chat
        self.channel = channel
        self.team_manager = TeamManager(self.chat, random_func=random_func)
        self.slack_client = slack_client
        self.handler = PendingStartHandler(self)
        self.board = Board(self.chat, random_func=random_func)
        self.clue_input_handler = None
        self.rand_func = random_func
        self.clue_number = None
        self.previous_handler = None
        if not self.rand_func:
            self.random_func = random
        
    def pending_start_complete(self):
        self.handler = GenerateGameHandler(self)
        
    def generate_game_complete(self):
        if not self.clue_input_handler:
            self.clue_input_handler = ClueInputHandler(self)
        self.handler = self.clue_input_handler
        
    def clue_input_complete(self, clue_number):
        self.clue_number = clue_number
        self.handler = GuessInputHandler(self, clue_number)
        
    def guess_input_complete(self):
        self.generate_game_complete()

    def interrupt_handler(self, handler):
        self.previous_handler = self.handler
        self.handler = handler

    def restore_handler(self):
        self.handler = self.previous_handler
        self.previous_handler = None

    def invalid_handler_complete(self):
        self.previous_handler = None
        self.handler = ResolveInvalidHandler(self)
        self.handler.start()

    def resolve_invalid_handler_complete(self):
        self.generate_game_complete()
