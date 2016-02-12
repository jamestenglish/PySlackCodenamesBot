from board import ASSASSIN_SPOT, BLUE_SPOT, RED_SPOT, BYSTANDER_SPOT, RED_TEAM, BLUE_TEAM
from game_end_exception import GameEndException

GUESS_COMMAND = 'cn guess'
GUESS_STOP_COMMAND = 'cn stop guess'


class GuessInputHandler:
    def __init__(self, game_state, clue_number):
        self.game_state = game_state
        self.max_guess_count = clue_number + 1
        self.guess_count = 1
        self.process_func = self._process_guess
        self.team_manager = game_state.team_manager
        self.board = game_state.board
        self.chat = game_state.chat
        
    def process(self, data):
        if self.process_func:
            self.process_func(data)
            
    def tick(self):
        pass
    
    def _process_guess(self, data):
        if self._is_guess_command(data) and self._is_current_player(data):
            if GUESS_STOP_COMMAND in data['text']:
                if self.guess_count < 1:
                    self.chat.message("You have to guess at least once!") 
                    return
                else:
                    return
            else:
                guess = data['text'].replace(GUESS_COMMAND, '').strip()
                if guess.upper() not in self.board.current_board:
                    self.chat.message("Invalid Guess, not a choice on the board! Try again")
                    return
                else:
                    self._process_valid_guess(guess)
                    return 
        elif self._is_guess_command(data) and not self._is_current_player(data):
            self.chat.message("Shush <@{}>! It's not your turn to guess!".format(data['user']))
            return    
        
    def _process_valid_guess(self, guess):
        secret = self.board.get_corresponding_secret(guess)
        if secret == ASSASSIN_SPOT:
            self._handle_assassin_guess(guess)
            return
        elif self._is_wrong_guess(guess, self.board.current_team):
            self._handle_wrong_guess(guess)
            return
        else:
            self._handle_correct_guess(guess)
            return

    def _handle_correct_guess(self, guess):
        print(str(self.guess_count))
        print(str(self.max_guess_count))
        self.board.update_board_reveal_secret(guess)
        self.board.display_board()
        
        if self.guess_count == self.max_guess_count:
            self.board.next_team()
            self.chat.message("No more guesses! On to the {}".format(self.board.current_team))
            print('done')
            self.game_state.guess_input_complete()
            return
        
        print('continue')
        self.guess_count += 1

    def _handle_assassin_guess(self, guess):
        self.board.update_board_reveal_secret(guess)
        self.board.display_board()
        self.chat.message("https://www.youtube.com/watch?v=1ytCEuuW2_A")
        losing_team = self.board.current_team
        self.board.next_team()
        winning_team = self.board.current_team
        self.chat.message("You picked the assassin! {} loses! {} wins!".format(losing_team, winning_team))
        raise GameEndException()
    
    def _handle_wrong_guess(self, guess):
        self.board.update_board_reveal_secret(guess)
        self.board.display_board()
        self.board.next_team()
        self.chat.message("Wrong answer! On to the {}".format(self.board.current_team))
        self.game_state.guess_input_complete()
        
    def _is_wrong_guess(self, guess, current_team):
        secret = self.board.get_corresponding_secret(guess)
        return secret == BYSTANDER_SPOT or ((current_team == RED_TEAM and secret == BLUE_SPOT) or (current_team == BLUE_TEAM and secret == RED_SPOT))

    def _is_current_player(self, data):
        return data['user'] in self.team_manager.get_operative_ids(self.board.current_team)

    def _is_guess_command(self, data):
        return 'text' in data \
            and 'channel' in data \
            and self.game_state.channel == data['channel'] \
            and (GUESS_COMMAND in data['text'].lower() or GUESS_STOP_COMMAND in data['text'].lower())\
            and ":" not in data['text']