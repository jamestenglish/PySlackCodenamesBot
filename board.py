import random
from wordlist import word_list


BLUE_TEAM = "Blue Team"
RED_TEAM = "Red Team"

RED_SPOT = ':red_circle:'
BLUE_SPOT = ':large_blue_circle:'
ASSASSIN_SPOT = ':black_circle:'
BYSTANDER_SPOT = ':white_circle:'

class Board:

    def __init__(self, chat, random_func=None):
        self.random = random
        if random_func:
            self.random = random_func
            
        self.chat = chat
        self.words = self.pick_words()
        
        self.current_team = self.random.choice([BLUE_TEAM, RED_TEAM])
        self.secret_board = self.pick_secret_board(self.current_team)
        self.current_board = list(self.words)         
        
    def pick_words(self):
        words = list(word_list)
        self.random.shuffle(words)
                
        return words[:25]
                
    def pick_secret_board(self, starting_team):
        status = []
        for _ in range(7):
            status.append(BYSTANDER_SPOT)
            
        red_count = 8
        blue_count = 8
        
        if starting_team is BLUE_TEAM:
            blue_count += 1
        else:
            red_count += 1
            
        for _ in range(red_count):
            status.append(RED_SPOT)
            
        for _ in range(blue_count):
            status.append(BLUE_SPOT)
            
        status.append(ASSASSIN_SPOT)
        
        self.random.shuffle(status)
                    
        return status 
    
    def _get_board_string(self, board):
        result = ""
        max_len = 0
        for word in board:
            if word[0] != ":" and len(word) > max_len:
                max_len = len(word)
        max_len += 2        
        for index, word in enumerate(board):
            if word[0] == ":":
                spaces = " ".join([""] * (max_len))
                result += "{}{}| ".format(word, spaces)
            else:
                result += "{}| ".format(word.ljust(max_len))
            if index != 0 and (index + 1) % 5 == 0:
                result += "\n"
                
        return result
    
    def _get_current_board_string(self):
        return self._get_board_string(self.current_board)
    
    def _get_secret_board_string(self):
        return self._get_board_string(self.secret_board)
    
    def display_board(self):
        self.chat.message(self._get_current_board_string)
        
    def display_secret_board(self, blue_spymaster, red_spymaster):
        message = "*Spymaster Board*:\n{}".format(self._get_secret_board_string())
        blue_spymaster.chat.message(message)
        red_spymaster.chat.message(message)
        
    def get_corresponding_secret(self, word):
        index = self.current_board.index(word.upper().strip())
        return self.secret_board[index]
        
    def update_board_reveal_secret(self, word):
        index = self.current_board.index(word.upper().strip())
        secret = self.secret_board[index]
        self.current_board[index] = secret
        
    def next_team(self):
        if self.current_team == BLUE_TEAM:
            self.current_team = RED_TEAM
        else:
            self.current_team = BLUE_TEAM

    def get_winner(self):
        total_blue_spots = self.secret_board.count(BLUE_SPOT)
        total_red_spots = self.secret_board.count(RED_SPOT)

        if self.current_board.count(BLUE_SPOT) == total_blue_spots:
            return BLUE_TEAM

        if self.current_board.count(RED_SPOT) == total_red_spots:
            return RED_TEAM

        return None

        
        

