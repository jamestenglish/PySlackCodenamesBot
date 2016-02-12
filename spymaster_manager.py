from board import BLUE_TEAM


class SpymasterManager:
    def __init__(self, game_state):
        self.game_state = game_state

    def get_spymaster(self):
        spymaster = self.game_state.team_manager.get_red_spymaster()
        if self.game_state.board.current_team is BLUE_TEAM:
            spymaster = self.game_state.team_manager.get_blue_spymaster()

        return spymaster

    def is_private_message(self, data):
        spymaster = self.get_spymaster()

        return 'channel' in data and 'text' in data and spymaster.get_im_channel() in data['channel']
