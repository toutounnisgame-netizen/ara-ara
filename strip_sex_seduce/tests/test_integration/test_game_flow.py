"""Tests intégration game flow"""

import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from entities.player import PlayerCharacter
from entities.npc import NPCMale
from systems.stats_system import StatsSystem

class TestGameFlow(unittest.TestCase):

    def setUp(self):
        self.player = PlayerCharacter("Test")
        self.npc = NPCMale()
        self.stats_system = StatsSystem()

    def test_npc_action_affects_player(self):
        initial_volonte = self.player.get_resistance_level()

        # Action NPC
        result = self.stats_system.apply_npc_action(
            self.player, 
            "compliment", 
            {"location": "bar", "privacy": 0.2}
        )

        self.assertTrue(result["success"])

        final_volonte = self.player.get_resistance_level()
        self.assertLess(final_volonte, initial_volonte)

if __name__ == '__main__':
    unittest.main()
