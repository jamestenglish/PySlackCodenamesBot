from game_state import GameState
from game_end_exception import GameEndException
from invalid_handler import InvalidHandler

class Game:
    def __init__(self, slack_client):
        self.slack_client = slack_client       
        self.game_state = GameState(slack_client)
        self.invalid_handler = InvalidHandler(self.game_state)

    def process(self, data):
        # TODO: quit handler
        try:
            is_invalid = self.invalid_handler.is_invalid(data)

            if is_invalid and not isinstance(self.game_state.handler, InvalidHandler):
                self.game_state.interrupt_handler(self.invalid_handler)
                self.invalid_handler.request_invalid_confirmation(data['user'])
            else:
                if self.game_state.handler:
                    self.game_state.handler.process(data)

        except GameEndException:
            self.__init__(self.slack_client)

    def tick(self):
        if self.game_state.handler:
            self.game_state.handler.tick()
