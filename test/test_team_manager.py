import unittest
from .mock_slack_client import MockSlackClient
from team_manager import TeamManager
from player import Player
from chat import Chat
from .random_mock import RandomMock


class TestTeamManager(unittest.TestCase):
    
    def test_add_player(self):
        
        slack_client = MockSlackClient()
        manager = TeamManager(Chat(slack_client, 'foo'))
        manager.add_player(Player("p1", slack_client))
        self.assertEqual(1, len(manager.players))
        self.assertEqual("You have joined the game!", slack_client.api_calls[-1][1])
    
    def test_multi_add(self):
        manager = TeamManager(RandomMock())
        slack_client = MockSlackClient()
        p1 = Player("p1", slack_client)
        manager.add_player(p1)
        manager.add_player(p1)
        self.assertEqual(1, len(manager.players))
    
    def test_pick_teams_odd(self):
        slack_client = MockSlackClient()
        manager = TeamManager(Chat(slack_client, 'foo'), RandomMock())
        
        manager.add_player(Player("p1", slack_client))
        manager.add_player(Player("p2", slack_client))
        manager.add_player(Player("p3", slack_client))
        manager.add_player(Player("p4", slack_client))
        manager.add_player(Player("p5", slack_client))
        
        manager.pick_teams()
        self.assertEqual(3, len(manager.blue_team))
        self.assertEqual(2, len(manager.red_team))
        self.assertEqual("p3", manager.blue_team[0].slack_id)
        self.assertEqual("p4", manager.blue_team[1].slack_id)
        self.assertEqual("p5", manager.blue_team[2].slack_id)
        
        self.assertEqual("p1", manager.red_team[0].slack_id)
        self.assertEqual("p2", manager.red_team[1].slack_id)
        
    def test_pick_teams_even(self):
        slack_client = MockSlackClient()
        manager = TeamManager(Chat(slack_client, 'foo'), RandomMock())
        
        manager.add_player(Player("p1", slack_client))
        manager.add_player(Player("p2", slack_client))
        manager.add_player(Player("p3", slack_client))
        manager.add_player(Player("p4", slack_client))
        
        manager.pick_teams()
        self.assertEqual(2, len(manager.blue_team))
        self.assertEqual(2, len(manager.red_team))
        
        self.assertEqual("p3", manager.blue_team[0].slack_id)
        self.assertEqual("p4", manager.blue_team[1].slack_id)
        
        self.assertEqual("p1", manager.red_team[0].slack_id)
        self.assertEqual("p2", manager.red_team[1].slack_id)
       
    def test_display_teams(self):
        slack_client = MockSlackClient()
        manager = TeamManager(Chat(slack_client, 'foo'), RandomMock())
        
        manager.add_player(Player("p1", slack_client))
        manager.add_player(Player("p2", slack_client))
        manager.add_player(Player("p3", slack_client))
        manager.add_player(Player("p4", slack_client))
        manager.add_player(Player("p5", slack_client))
        
        manager.pick_teams()
        manager.display_teams()
        red_team = "*Red Spymaster:*\np1\n\n*Red Field Operatives:\n*p2\n"
        blue_team = "*Blue Spymaster:*\np3\n\n*Red Field Operatives:\n*p4\np5\n"

        self.assertEqual(red_team, slack_client.api_calls[-1][1])
        self.assertEqual(blue_team, slack_client.api_calls[-4][1])
        
    def test_get_spymasters(self):
        slack_client = MockSlackClient()
        manager = TeamManager(Chat(slack_client, 'foo'), RandomMock())
        
        p1 = Player("p1", slack_client)
        p3 = Player("p3", slack_client)
        manager.add_player(p1)
        manager.add_player(Player("p2", slack_client))
        manager.add_player(p3)
        manager.add_player(Player("p4", slack_client))
        manager.add_player(Player("p5", slack_client))
        
        manager.pick_teams()
        self.assertEqual(p1, manager.get_red_spymaster())
        self.assertEqual(p3, manager.get_blue_spymaster())
        