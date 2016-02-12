from game_state import GameState
from game_end_exception import GameEndException


class Game:
    def __init__(self, slack_client):
        self.slack_client = slack_client       
        self.game_state = GameState(slack_client)

    def process(self, data):
        # TODO: invalid clue handler
        # TODO: quit handler
        try:
            if self.game_state.handler:
                self.game_state.handler.process(data)
        except GameEndException:
            self.__init__(self.slack_client)

    
    def tick(self):
        if self.game_state.handler:
            self.game_state.handler.tick()
            

        
        
        
        