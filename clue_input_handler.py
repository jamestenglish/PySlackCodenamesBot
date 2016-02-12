from spymaster_manager import SpymasterManager
from guess_input_handler import GUESS_COMMAND, GUESS_STOP_COMMAND

INVALID_CLUE_COMMAND = "cn invalid clue"


class ClueInputHandler:
    def __init__(self, game_state):
        self.game_state = game_state
        self.tick_func = self._solicit_word_tick
        self.process_func = None
        self.clue_word = None
        self.clue_num = None
        self.spymaster_manager = SpymasterManager(game_state)
    
    def process(self, data):
        if self.process_func:
            self.process_func(data)
    
    def tick(self):
        if self.tick_func:
            self.tick_func()
    
    def _solicit_word_tick(self):
        spymaster = self.spymaster_manager.get_spymaster()
            
        self.process_func = self._process_word
        
        spymaster.chat.message("What is your one word clue?")
            
        self.tick_func = None
        
    def _process_word(self, data):
        spymaster = self.spymaster_manager.get_spymaster()
        if self.spymaster_manager.is_private_message(data):
            text = data['text'].strip()
            if len(text.split(" ")) > 1:
                spymaster.chat.message("Invalid input! One word only! Please try again...")
            else:
                self.clue_word = text
                self.process_func = self._process_number
                spymaster.chat.message("What is your clue number? [0-999]")

    def _process_number(self, data):
        if self.spymaster_manager.is_private_message(data):
            text = data['text'].strip()
            guess_count = 0
    
            try:
                guess_count = int(text)
            except ValueError:
                spymaster = self.spymaster_manager.get_spymaster()
                spymaster.chat.message("Invalid Input! Enter a number [0-999]")
                return
                
            self.clue_num = text
            self._display_clue(self.clue_word, self.clue_num)    
            self.game_state.clue_input_complete(guess_count)
            
    def _display_clue(self, clue_word, clue_num):
        self.game_state.chat.message("*{}:* your clue is: `{} {}`".format(self.game_state.board.current_team, clue_word, clue_num))
        self.game_state.chat.message("If you feel the clue is against the rules message `{}`\nTo guess use `{} WORD`\nTo stop guessing use: `{}`\nRemember anyone on your team can guess, so consult carefully before guessing!".format(INVALID_CLUE_COMMAND, GUESS_COMMAND, GUESS_STOP_COMMAND))
                
                