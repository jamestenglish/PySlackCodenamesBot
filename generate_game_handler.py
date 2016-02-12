
class GenerateGameHandler:
    def __init__(self, game_state):
        self.game_state = game_state
        
    def process(self, data):
        pass
            
    def tick(self):
        self.game_state.chat.message("Starting game, picking teams, generating board!")
        self.game_state.chat.message("Remember when it is your teams turn *anyone* can guess using `cn guess TARGET` so deliberate carefully!")
        self._pick_teams()
        self.game_state.team_manager.display_teams()
        self.game_state.board.display_board()
        blue_spymaster = self.game_state.team_manager.get_blue_spymaster()
        red_spymaster = self.game_state.team_manager.get_red_spymaster()
        self.game_state.board.display_secret_board(blue_spymaster, red_spymaster)
        self.game_state.generate_game_complete()
        
        
    def _pick_teams(self):
        self.game_state.team_manager.pick_teams()