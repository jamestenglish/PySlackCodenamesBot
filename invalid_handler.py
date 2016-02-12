from clue_input_handler import INVALID_CLUE_COMMAND

INVALID_CLUE_CONFIRM_COMMAND = "cn invalid agree"


class InvalidHandler:
    def __init__(self, game_state):
        self.game_state = game_state
        self.chat = game_state.chat
        self.count = 0
        self.user = None
        self.last_message = None
        self.message_template = "Is the clue against the rules? Reply `{}` to confirm in {} seconds"

    def is_invalid(self, data):
        return 'text' in data \
               and INVALID_CLUE_COMMAND in data['text'] \
               and self.game_state.channel == data['channel']

    def process(self, data):
        if 'text' in data \
                and 'channel' in data \
                and data['channel'] == self.game_state.channel \
                and INVALID_CLUE_CONFIRM_COMMAND in data['text']:

            self.game_state.board.next_team()
            self.chat.message("Clue deemed invalid! {} will gets a freebie".format(self.game_state.board.current_team))
            self.game_state.invalid_handler_complete()

    def tick(self):
        self.count -= 1
        if self.count == 0:
            self.game_state.restore_handler()
            return

        message = self.message_template.format(INVALID_CLUE_CONFIRM_COMMAND, self.count)
        self.last_message = self.chat.message(message, self.last_message)

    def request_invalid_confirmation(self, user):
        self.count = 30
        self.last_message = self.chat.message(self.message_template.format(INVALID_CLUE_CONFIRM_COMMAND, self.count))
        self.user = user

