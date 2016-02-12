from functools import partial
from chat import Chat
from player import Player
from game_end_exception import GameEndException

JOIN_COMMAND = "cn join"
START_COMMAND = "cn start"

class PendingStartHandler:
    def __init__(self, game_state):
        self.game_state = game_state
        self.process_func = self._process_pending_start
        self.tick_func = None
    
    def process(self, data):
        if self.process_func:
            self.process_func(data)
            
    def tick(self):
        if self.tick_func:
            self.tick_func()
        
    def _process_pending_start(self, data):
        if 'text' in data and 'channel' in data:
            if START_COMMAND in data['text'].lower():
                self._solict_players(data)
                
    def _solict_players(self, data):
        self.game_state.channel = data['channel']
        self.game_state.chat = Chat(self.game_state.slack_client, self.game_state.channel)
        self.process_func = self._process_player_join
        self.tick_func = partial(self._solicit_player_countdown_tick, remaining=30, last_message=None)
        
    def _process_player_join(self, data):
        if 'text' in data and 'channel' in data and self.game_state.channel == data['channel']:
            if JOIN_COMMAND in data['text']:
                player = Player(data['user'], self.game_state.slack_client)
                self.game_state.team_manager.add_player(player)

    def _solicit_player_countdown_tick(self, remaining, last_message):
        if remaining == 0:
            if len(self.game_state.team_manager.players) < 4:
                self.game_state.chat.message("Game needs at least 4 players, not enough joined to start")
                raise GameEndException()

            self.game_state.pending_start_complete()
            return
        
        last_message = self.game_state.chat.message("Starting Codenames game in {} seconds. Reply `{}` to play".format(remaining, JOIN_COMMAND), last_message)
        
        self.tick_func = partial(self._solicit_player_countdown_tick, remaining=(remaining - 1), last_message=last_message)