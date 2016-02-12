import random

from board import RED_TEAM

class TeamManager:
    def __init__(self, chat, random_func=None):
        self.players = []
        self.red_team = []
        self.blue_team = []
        self.random = random
        self.chat = chat
        if random_func:
            self.random = random_func
        
    def add_player(self, player):
        if player not in self.players:
            self.players.append(player)
            player.chat.message("You have joined the game!")
            
    def pick_teams(self):
        shuffled_players = list(self.players)
        self.random.shuffle(shuffled_players)
        half = len(shuffled_players) // 2
        
        self.blue_team = shuffled_players[half:]
        self.red_team = shuffled_players[:half]
        
    def display_teams(self):
        self._display_team("Blue", self.blue_team)
        self._display_team("Red", self.red_team)
        
    def _display_team(self, color, team):
        field_operatives = ""
        for player in team[1:]:
            field_operatives += "{}\n".format(player.get_username())

        message = "*{} Spymaster:*\n{}\n\n*Red Field Operatives:\n*{}"
        self.chat.message(message.format(color,team[0].get_username(), field_operatives))
        
    def get_red_spymaster(self):
        return self.red_team[0]
    
    def get_blue_spymaster(self):
        return self.blue_team[0]
    
    def get_operative_ids(self, team):
        operative_ids = []
        
        if team == RED_TEAM:
            for player in self.red_team[1:]:
                operative_ids.append(player.slack_id)
        else:
            for player in self.blue_team[1:]:
                operative_ids.append(player.slack_id)
                
        return operative_ids
