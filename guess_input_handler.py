from board import ASSASSIN_SPOT, BLUE_SPOT, RED_SPOT, BYSTANDER_SPOT, RED_TEAM, BLUE_TEAM
from game_end_exception import GameEndException

GUESS_COMMAND = 'cn guess'
GUESS_STOP_COMMAND = 'cn stop guess'


class GuessInputHandler:
    def __init__(self, game_state, clue_number):
        self.game_state = game_state
        self.max_guess_count = clue_number + 1
        self.guess_count = 1
        self.team_manager = game_state.team_manager
        self.board = game_state.board
        self.chat = game_state.chat
            
    def tick(self):
        pass
    
    def process(self, data):
        if self._is_guess_command(data) and self._is_current_player(data):
            if GUESS_STOP_COMMAND in data['text']:
                self._process_stop()
            else:
                self._process_guess(data)
        elif self._is_guess_command(data) and not self._is_current_player(data):
            self.chat.message("Shush <@{}>! It's not your turn to guess!".format(data['user']))

    def _process_guess(self, data):
        guess = data['text'].replace(GUESS_COMMAND, '').strip()
        if guess.upper() not in self.board.current_board:
            self.chat.message("Invalid Guess, not a choice on the board! Try again")
        else:
            self._process_valid_guess(guess)

    def _process_stop(self):
        if self.guess_count < 2:
            self.chat.message("You have to guess at least once!")
        else:
            self._process_stop_success()

    def _process_stop_success(self):
        self.board.display_board()
        self.board.next_team()
        self.chat.message("Ok on to {}".format(self.board.current_team))
        self.game_state.guess_input_complete()

    def _process_valid_guess(self, guess):
        secret = self.board.get_corresponding_secret(guess)
        if secret == ASSASSIN_SPOT:
            self._handle_assassin_guess(guess)
        elif self._is_wrong_guess(guess, self.board.current_team):
            self._handle_wrong_guess(guess)
        else:
            self._handle_correct_guess(guess)

    def _handle_correct_guess(self, guess):
        self.chat.message("Correct! You have {} more guesses.".format(self.max_guess_count- self.guess_count))

        self.board.update_board_reveal_secret(guess)
        self.board.display_board()

        self._handle_if_win()

        if self.guess_count == self.max_guess_count:
            self.board.next_team()
            self.chat.message("No more guesses! On to the {}".format(self.board.current_team))
            self.game_state.guess_input_complete()
        else:
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

        self._handle_if_win()

        self.board.next_team()
        self.chat.message("Wrong answer! On to the {}".format(self.board.current_team))
        self.game_state.guess_input_complete()

    def _handle_if_win(self):
        winner = self.board.get_winner()
        if winner is not None:
            self.chat.message("GAME OVER! {} WINS!".format(winner))
            raise GameEndException()

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