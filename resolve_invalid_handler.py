from spymaster_manager import SpymasterManager


class ResolveInvalidHandler:
    def __init__(self, game_state):
        self.game_state = game_state
        self.board = game_state.board
        self.spymaster_manager = SpymasterManager(game_state)
        self.chat = game_state.chat

    def start(self):
        spymaster = self.spymaster_manager.get_spymaster()
        spymaster.chat.message("Pick a word to reveal:")

    def process(self, data):
        if self.spymaster_manager.is_private_message(data):
            word = data['text'].upper().strip()
            if word not in self.board.current_board or word[0] == ":":
                spymaster = self.spymaster_manager.get_spymaster()
                spymaster.chat.message("Invalid! Please try again...")
            else:
                self.board.update_board_reveal_secret(word)
                self.chat.message("Still {}'s turn. Getting next clue...".format(self.board.current_team))
                self.game_state.resolve_invalid_handler_complete()

